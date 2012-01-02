#! /usr/bin/env python3
import os
import subprocess
from optparse import OptionParser

from .bzr_dir import BazaarDir
from .git_dir import GitDir
from .rsync_dir import RsyncDir
from .s3_cmd_dir import S3CmdDir
from .s3_rsync_dir import S3RsyncDir

protocols = {
    "rsync": RsyncDir,
    "git": GitDir,
    "bzr": BazaarDir,
    "bazaar": BazaarDir,
    "s3cmd": S3CmdDir,
    "s3rsync": S3RsyncDir,
    }

def main():
    parser = OptionParser()

    parser.add_option("-n", "--no-delete", action="store_true", 
        dest="NO_DELETE", default=False, 
        help="Don't deleted orphaned files on remote machince after transfer.")
    parser.add_option("-e", "--edit", action="store_true", 
        dest="EDIT", default=False, 
        help="Open and edit the configuration file.")

    (options, args) = parser.parse_args()

    # Initialize
    backup_dirs = []

    protocol_name = None
    protocol_args = None

    HOME = os.getenv("HOME")

    cmd_line_options = {'NO_DELETE': options.NO_DELETE}

    # Editor mode
    if options.EDIT:
        EDITOR = os.getenv("EDITOR")

        if EDITOR == "":
            print("EDITOR enviromental variable not set!")
            return

        if not os.path.exists(HOME + "/.config/pybackup/"):
            os.makedirs(HOME + "/.config/pybackup/")

        subprocess.call("{0} {1}/.config/pybackup/folders.txt".format(EDITOR, HOME), shell=True)
        print("Edited configuration file {0}/.config/pybackup/folders.txt".format(HOME))
        return

    #Read in the file
    with open('{0}/.config/pybackup/folders.txt'.format(HOME), 'r') as folderfile:
        lines = [line.strip() for line in folderfile]
    lines = [line.partition("#")[0] for line in lines if not line.startswith("#")]

    for line in lines:
        ls = line.split()
        if len(ls) == 0:
            continue
        elif ls[0].lower() in protocols:
            protocol_name = ls[0].lower()
            protocol_args = ls[1:]
        else:
            dir_args = ls + protocol_args
            backup_dirs.append( protocols[protocol_name](*dir_args, **cmd_line_options) )

    # Run the backups
    last_id = id(backup_dirs[-1])
    for bd in backup_dirs:
        bd.backup()
        if id(bd) != last_id:
            print("")
    
    return
        
if __name__ == "__main__":
    main()
