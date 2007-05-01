#!/usr/bin/env python

"""
   Usage: i18ngenerate.py 

   This is just a simple wrapper script for i18ngenerator.
"""

import os, sys, shutil

__PYTHON = os.environ.get('PYTHON', 'python')

def main():

    # go to the tests folder

    os.chdir('..')
    os.chdir('tests')

    if not os.path.isfile('i18ngenerator.py'):
        print 'i18ngenerator was not found.'
        sys.exit(1)

    os.system(__PYTHON + ' i18ngenerator.py')

    # now move the generated pots to the i18n folder

    files = os.listdir(os.curdir)
    files = [f for f in files if f.endswith('.pot')]

    target = '..' + os.sep + 'i18n' + os.sep
    for file in files:
        if os.path.exists(target+file):
            os.remove(target+file)
        shutil.move(file, target)

if __name__ == '__main__':
    main()
