#!/usr/bin/env python

"""
   Usage: sync.py [<product> | <language-code>]
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys
from utils import getPoFilesAsCmdLine, getPoFilesByLanguageCode, getProduct, getPotFiles, getLongProductName

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) == 1:
        print 'You have to specify a product or a language code.'
        sys.exit(1)

    product = getLongProductName(sys.argv[1])
    pot = '%s.pot' % product

    os.chdir('..')

    if not os.path.isfile(pot): # no pot? test for language-code
        poFiles = getPoFilesByLanguageCode(product)
        if poFiles:
            potFiles = getPotFiles()
            for po in poFiles:
                for pot in potFiles:
                    if getProduct(po) == getProduct(pot):
                        os.system(__PYTHON + ' ' + __I18NDUDE + (' sync --pot %s %s') % (pot, po))
        else:
            print 'Neither a pot nor po files for the given argument were found.'
            sys.exit(3)

    else: # product was given
        poFiles = getPoFilesAsCmdLine(product)
        if poFiles == []:
            print 'No po-files were found for the given product.'
            sys.exit(4)

        os.system(__PYTHON + ' ' + __I18NDUDE + (' sync --pot %s %s') % (pot, poFiles))

if __name__ == '__main__':
    main()
