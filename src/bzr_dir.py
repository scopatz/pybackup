import os
import time
import subprocess

class BazaarDir(object):
    def __init__(self, ld, pl, *args, **kw):
        self.localdir = ld
        self.pushloc  = pl
        return

    def __str__(self):
        s = "Local Directory:\t{localdir!s}\n"
        s = s + "Push Location:\t{pushloc!s}\n"
        return s.format(**self.__dict__)

    def backup(self):
        startstr = "Starting push from \033[1;36m{localdir!s}\033[1;32m to \033[1;35m{pushloc!s}\033[1;32m...".format(**self.__dict__)
        print("\033[1;32m{}\033[0m".format(startstr))
        t1 = time.time()

        origdir = os.getcwd()        

        try:
            os.chdir(self.localdir)
            subprocess.call("bzr push {pushloc}".format(**self.__dict__), shell=True)
            t2 = time.time()
            print("\033[1;32m{0:{1}}...Completed in \033[1;33m{2:.3G}\033[1;32m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )
        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        os.chdir(origdir)
        return    
