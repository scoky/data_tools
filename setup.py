#!/usr/bin/env python

from distutils.core import setup

def get_scripts():
    import glob
    return [f for f in glob.glob('scripts/*.py') if '__' not in f]

setup(
      scripts=get_scripts()
     )
