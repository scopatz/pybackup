#! /usr/bin/env python3
import os
import subprocess
from optparse import OptionParser

from rsync_dir import RsyncDir
from bzr_dir   import BazaarDir
from git_dir   import GitDir

def main():
    parser = OptionParser()

    parser.add_option("-n", "--no-delete", action="store_true", 
        dest="NoDeleteAfter", default=False, 
        help="Don't deleted orphaned files on remote machince after transfer.")
    parser.add_option("-e", "--edit", action="store_true", 
        dest="Edit", default=False, 
        help="Open and edit the configuration file.")

    (options, args) = parser.parse_args()

    #Iinitialize
    backup_dirs = []

    REMOTE = ""

    REMOTEUSER = ""
    REMOTEHOST = ""

    HOME = os.getenv("HOME")

    # Editor mode
    if options.Edit:
        EDITOR = os.getenv("EDITOR")

        if EDITOR == "":
            print("EDITOR enviromental variable not set!")
            return

        subprocess.call("{0} {1}/.backup/folders.txt".format(EDITOR, HOME), shell=True)
        print("Edited configuration file {0}/.backup/folders.txt".format(HOME))
        return

    #Read in the file
    with open('{0}/.backup/folders.txt'.format(HOME), 'r') as folderfile:
        for line in folderfile:
            ls = line.split()
            if len(ls) == 0:
                REMOTE = ""
                REMOTEUSER = ""
                REMOTEHOST = ""
            elif ls[0][0] == "#":
                continue

            #Determine REMOTE type            
            elif ls[0].upper() == "RSYNC":
                REMOTE     = "RSYNC"
                REMOTEUSER = ls[1]
                REMOTEHOST = ls[2]
            elif ls[0].upper() == "BAZAAR":
                REMOTE = "BAZAAR"
            elif ls[0].upper() == "BZR":
                REMOTE = "BAZAAR"
            elif ls[0].upper() == "GIT":
                REMOTE = "GIT"

            #Rsync the directory
            elif (REMOTE == "RSYNC") and (len(ls) == 1):
                backup_dirs.append( rsync_dir(ls[0], ls[0], REMOTEUSER, REMOTEHOST) )

            elif (REMOTE == "RSYNC") and (len(ls) == 2):
                if (ls[-1].upper() == "D") :
                    if options.NoDeleteAfter:
                        backup_dirs.append( RsyncDir(ls[0], ls[0], REMOTEUSER, REMOTEHOST, False) )
                    else:
                        backup_dirs.append( RsyncDir(ls[0], ls[0], REMOTEUSER, REMOTEHOST, True) )
                else:
                    backup_dirs.append( RsyncDir(ls[0], ls[1], REMOTEUSER, REMOTEHOST) )

            elif (REMOTE == "RSYNC") and (len(ls) == 3):
                if (ls[-1].upper() == "D") and (not options.NoDeleteAfter):
                    backup_dirs.append( RsyncDir(ls[0], ls[1], REMOTEUSER, REMOTEHOST, True) )
                else:
                    backup_dirs.append( RsyncDir(ls[0], ls[1], REMOTEUSER, REMOTEHOST, False) )

            # Use Bazaar to push the directory
            elif (REMOTE == "BAZAAR"):
                backup_dirs.append( BazaarDir(ls[0], ls[1]) )

            # Use Git to push the directory
            elif (REMOTE == "GIT"):
                message = ""
                if 1 < len(ls):
                    message = line[line.find(ls[0])+len(ls[0]):-1]
                    message = message[message.find(ls[1]):]
                backup_dirs.append( GitDir(ls[0], message) )

            else:
                print("\033[1;31mFailed\033[0m to add the following directory to the list of files to sync:\033[1;36m", line, "\033[0m")

    #Run the backups
    n = 0
    while n < len(backup_dirs):
        if n != 0:
            print("")
        backup_dirs[n].backup()
        n = n + 1
    
    return
        
if __name__ == "__main__":
    main()
