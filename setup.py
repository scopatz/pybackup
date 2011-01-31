#!/usr/bin/env python3
 
from distutils.core import setup
from distutils.extension import Extension
from setuptools.command.develop import develop


setup(name="pybackup",
	version='0.3',
	description='A command-line utility to handle backing up of multiple directories over multiple protocols.',
	author='Anthony Scopatz',
	author_email='scopatz@gmail.com',
	url='http://www.scopatz.com/',
	packages=['pybackup', ],
	package_dir={'pybackup': 'src'}, 
	package_data={'': []},
    scripts=['src/scripts/pybackup'],
	)

