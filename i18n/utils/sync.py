#!/usr/bin/env python

"""
   Usage: sync.py <product>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys
from utils import getPoFilesAsCmdLine

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) == 1:
        print 'You have to specify the product.'
        sys.exit(1)

    product = sys.argv[1]

    if product in ['atct', 'atrbw', 'at']:
        if product == 'at':
            product = 'archetypes'
        elif product == 'atct':
            product = 'atcontenttypes'
        else:
            product = 'atreferencebrowserwidget'

    pot = '%s.pot' % product

    os.chdir('..')

    if not os.path.isfile(pot):
        print 'No pot was found for the given product.'
        sys.exit(2)

    poFiles = getPoFilesAsCmdLine(product)
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(3)

    os.system(__PYTHON + ' ' + __I18NDUDE + (' sync --pot %s -s %s') % (pot, poFiles))

if __name__ == '__main__':
    main()
