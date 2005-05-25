#!/usr/bin/env python

"""
   Usage: sync.py <product>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def getPoFiles(product):
    files = os.listdir(os.curdir)
    files = [file for file in files if file.startswith(product) and file.endswith('.po') and file != '%s-en.po' % product]
    filestring = ''
    for file in files:
        filestring += file + ' '
    return filestring.rstrip()

def main():
    if len(sys.argv) == 1:
        print 'You have to specify the product.'
        sys.exit(1)

    product = sys.argv[1]
    pot = '%s.pot' % product

    os.chdir('..')

    if not os.path.isfile(pot):
        print 'No pot was found for the given product.'
        sys.exit(2)

    poFiles = getPoFiles(product)
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(3)

    os.system(__PYTHON + ' ' + __I18NDUDE + (' sync --pot %s -s %s') % (pot, poFiles))

if __name__ == '__main__':
    main()
