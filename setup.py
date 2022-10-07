#!/usr/bin/env python

from distutils.core import setup

def get_scripts():
    import glob
    return [f for f in glob.glob('scripts/*.py') if '__' not in f]

setup(name='data_tools',
      version='1.0',
      description='Useful generic python scripts for working with text files from the command line',
      author='Kyle Schomp',
      author_email='kyle.schomp@gmail.com',
      packages=['data_tools'],
      scripts=get_scripts()
     )
