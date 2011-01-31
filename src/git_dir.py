import os
import time
import subprocess

class GitDir(object):
    def __init__(self, ld, pm):
        self.localdir = ld
        self.push_message  = str(pm)

        if self.push_message != "":
            self.push_message = self.push_message + " "
        self.push_message = self.push_message + "(Pybackup autopush at {0})".format(time.ctime())
        return

    def __str__(self):
        s = "Local Directory:\t{localdir!s}\n"
        s = s + "Push Message:\t{push_message!s}\n"
        return s.format(**self.__dict__)

    def backup(self):
        startstr = "Starting git push from \033[1;36m{localdir!s}\033[1;32m...".format(**self.__dict__)
        print("\033[1;32m{}\033[0m".format(startstr))
        t1 = time.time()

        origdir = os.getcwd()        

        os.chdir(self.localdir)

        # get status of this repository
        print("\033[0;32m ~~~ Git Status ~~~\033[0m")
        try:
            subprocess.call("git status", shell=True)
            git_status = subprocess.getoutput("git status -s")
            git_status = git_status.split('\n')
        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed while trying to get git status after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        # Check that there are non-trivial updates
        git_status_good = []
        git_status_bad  = []
        for line in git_status:
            if "??" in line:
                git_status_bad.append(line)
            else:
                git_status_good.append(line)

        if not (git_status_bad == []):
            print("\033[0;31mPybackup/Git does not know how to deal with the following files:\033[0m")
            for line in git_status_bad:
                print("    {0}".format(line))
            print("\033[0;31mThese files should be explicitly added to the repository using 'git add <file>'\033[0m")

        if (git_status_good == []) or (git_status_good == ['']):
            t2 = time.time()
            print("\033[0;32m{0:{1}}...Repository is already up-to-date. Completed in \033[1;33m{2:.3G}\033[1;32m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )
            os.chdir(origdir)
            return

        # Commit to this repository
        print("\033[0;32m ~~~ Git Commit with message: {0} ~~~\033[0m".format(self.push_message))
        try:
            subprocess.call("git commit -a -m '{0}'".format(self.push_message), shell=True)
        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed while trying to get git status after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        # Push to the remote repository
        print("\033[0;32m ~~~ Git Push ~~~\033[0m".format(self.push_message))
        try:
            subprocess.call("git push -v", shell=True)
        except:
            t2 = time.time()
            print("\033[1;31m{0:{1}}...Failed while trying to push git to remote repository after \033[1;33m{2:.3G}\033[1;31m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        # Completed sucessfully
        t2 = time.time()
        print("\033[1;32m{0:{1}}...Completed in \033[1;33m{2:.3G}\033[1;32m min!\033[0m".format("", len(startstr)-3-28, (t2-t1)/60.0) )

        os.chdir(origdir)
        return    
