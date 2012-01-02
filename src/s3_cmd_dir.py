import os
import time
import subprocess

class S3CmdDir(object):
    def __init__(self, *args, **kw):
        self.localdir = args[0]
        self.command = kw['CMD']

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

        self.bucket = args[-2]
        self.mount_point = args[-1] 

        if self.remotedir.startswith("/"):
            self.remotedir = self.remotedir[1:]
        self.remotedir = os.path.join(self.bucket, self.remotedir)
        self.deleteflag = ((df.upper() == "D") and (not kw['NO_DELETE']))
        return

    def __str__(self):
        s = "Local Directory:\t{localdir!s}\n"
        s = s + "Remote Directory:\t{remotedir!s}\n"
        s = s + "Bucket:\t\t{bucket!s}\n"
        s = s + "Mount Point:\t\t{mount_point}\n"
        s = s + "Delete Abandoned Files:\t\t{deleteflag}\n"
        return s.format(**self.__dict__)

    def backup(self):
        startstr = "Starting transfer from \033[1;36m{localdir!s}\033[1;32m to \033[1;35m{remotedir!s}\033[1;32m...".format(**self.__dict__)
        print("\033[1;32m{}\033[0m".format(startstr))
        t1 = time.time()

        # Build command
        cmd = "s3cmd -rvFH --progress"

        if self.deleteflag:
            cmd += " --delete-removed"

        if self.command == "push":
            cmd += " sync {localdir} s3://{remotedir}".format(**self.__dict__)
        elif self.command == "pull":
            cmd += " sync s3://{remotedir} {localdir}".format(**self.__dict__)
            if not os.path.exists(self.localdir):
                os.makedirs(self.localdir)

        # Run the sync command
        try:
            subprocess.call(cmd, shell=True)
            t2 = time.time()
            print("\033[1;32m{0:{1}}...Completed in \033[1;33m{2:.3G}\033[1;32m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )
        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )
        return    


