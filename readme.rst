*******************
Welcome to Pybackup
*******************

Pybackup is a command line utility that was created to automate much of the 
local-to-remote backup procedure. It has the ability to easily handle many 
directories that need to go to several places over a variety of secure protocols.  

Currently, Pybackup supports the following file transfer systems:

  1. rsync
  2. git
  3. bzr (bazaar)
  4. s3rsync (Amazon's S3 via s3fs and rynsc)
  5. s3cmd (Amazon's S3 via the s3cmd utility)

More transfer mechanisms (such as hg, svn, scp) could be added with ease, if
needed.  Each of these methods require that the local host and the remote 
server be configured properly.  Additionally, public RSA keys for SSL must 
be set up prior to use.

------------
Installation
------------

**Step 1:** Download and place the files here in a directory somewhere on your
local machine.

**Step 2:** Link backup.py to somewhere on your PATH (you may need to be root)::

    ln -s /usr/bin/pybackup /path/to/backup.py

**Step 3:** Configure ``~/.backup/folders.txt``.  You may use ``folders.txt.example`` 
as a template.

**Step 4:** ???

**Step 5:** Profit.


-----
Usage
-----

At any time from the command line, you may backs up all of the folders listed 
in ``folders.txt`` by running::

    $ pybackup


Additionally, you may quickly edit ``folders.txt`` by running::

    $ pybackup -e 


-------------------
Configuration Notes
-------------------

Please see ``folders.txt.example`` for a description of how to configure Pybackup.
However, some subtleties are worth pointing out here.

All directories in the block below a remote transfer name (e.g. RSYNC) are 
copied using this program.  Blocks are ended by declaring another transfer mechanism
(e.g. GIT).  Some transfer types have associated arguments that are also required
to execute.  Transfer type names are case insensitive.  So ``"git"``, ``"GIT"``,
``"gIt"``, etc are all valid.

For RSYNC, you can choose to remove files on the remote server that are no longer 
locally present.  To do this, simply append a ``"D"`` or ``"d"`` after the folder
specification.

If you want to temporarily disable backing up a folder, you may comment it out 
by placing the standard hash symbol ``"#"`` at the beginning of the line.

If there are uncommitted changes in a GIT directory, it will auto-commit and auto-push 
any modified files.  New files that are untracked by the git repository will be 
skipped.  This behavior is useful for trivial changes, but dangerous for more
significant ones. Be careful!
