import os
import time
import subprocess

class RsyncDir(object):
    def __init__(self, ld, rd, ru, rh, df=False):
        self.localdir   = ld
        self.remotedir  = rd
        self.remoteuser = ru
        self.remotehost = rh
        self.deleteflag = df
        return

    def __str__(self):
        s = "Local Directory:\t{localdir!s}\n"
        s = s + "Remote Directory:\t{remotedir!s}\n"
        s = s + "Remote User:\t\t{remoteuser!s}\n"
        s = s + "Remote Host:\t\t{remotehost!s}\n"
        s = s + "Remote Host:\t\t{deleteflag}\n"
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
