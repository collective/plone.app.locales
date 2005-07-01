#!/usr/bin/env python

"""
   Usage: chart.py <product>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys
from utils import getPoFilesAsCmdLine, getLongProductName

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) == 1:
        print 'You have to specify the product.'
        sys.exit(1)

    product = getLongProductName(sys.argv[1])
    pot = '%s.pot' % product
    chart = os.curdir + os.sep + 'charts' + os.sep + '%s-chart.gif' % product

    os.chdir('..')

    if not os.path.isfile(pot):
        print 'No pot was found for the given product.'
        sys.exit(2)

    poFiles = getPoFilesAsCmdLine(product)
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(3)

    os.system(__PYTHON + ' ' + __I18NDUDE + (' chart -o %s --pot %s %s') % (chart, pot, poFiles))

if __name__ == '__main__':
    main()
