#!/usr/bin/env python3
 
from distutils.core import setup


if __name__ == '__main__':
    setup(name="pybackup",
	    version='0.3',
	    description='A command-line utility to handle backing up of multiple directories over multiple protocols.',
	    author='Anthony Scopatz',
	    author_email='scopatz@gmail.com',
	    url='http://www.scopatz.com/',
	    packages=['pybackup', ],
	    package_dir={'pybackup': 'src'}, 
	    package_data={'': []},
        scripts=['src/scripts/pybackup', 'src/scripts/gmail-backup'],
	    )

