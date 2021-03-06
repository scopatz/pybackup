import os
import time
import subprocess

class RsyncDir(object):
    def __init__(self, *args, **kw):
        self.localdir = args[0]

        mid_args = args[1:-2]
        if len(mid_args) == 0: 
            self.remotedir = self.localdir
            df = "N"
        if len(mid_args) == 1: 
            self.remotedir = mid_args[0] if len(mid_args[0]) != 1 else self.localdir
            df = mid_args[0] if len(mid_args[0]) == 1 else "N"
        elif len(mid_args) == 2:
            self.remotedir = mid_args[0]
            df = mid_args[1]
        else:
            raise ValueError("Too many arguments for " + repr(self.localdir))

        self.deleteflag = ((df.upper() == "D") and (not kw['NO_DELETE']))

        self.remoteuser = args[-2]
        self.remotehost = args[-1]
        return

    def __str__(self):
        s = "Local Directory:\t{localdir!s}\n"
        s = s + "Remote Directory:\t{remotedir!s}\n"
        s = s + "Remote User:\t\t{remoteuser!s}\n"
        s = s + "Remote Host:\t\t{remotehost!s}\n"
        s = s + "Delete Abandoned Files:\t\t{deleteflag}\n"
        return s.format(**self.__dict__)

    def backup(self):
        startstr = "Starting transfer from \033[1;36m{localdir!s}\033[1;32m to \033[1;35m{remotehost!s}\033[1;32m...".format(**self.__dict__)
        print("\033[1;32m{}\033[0m".format(startstr))
        t1 = time.time()

        try:
            if self.deleteflag:
                cmd = "rsync --stats --progress --partial -h --rsh=ssh -avrlLH --delete-after {localdir} {remoteuser}@{remotehost}:{remotedir}".format(**self.__dict__)
            else:
                cmd = "rsync --stats --progress --partial -h --rsh=ssh -avrlLH {localdir} {remoteuser}@{remotehost}:{remotedir}".format(**self.__dict__)

            subprocess.call(cmd, shell=True)
            t2 = time.time()

            print("\033[1;32m{0:{1}}...Completed in \033[1;33m{2:.3G}\033[1;32m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )
        return    
