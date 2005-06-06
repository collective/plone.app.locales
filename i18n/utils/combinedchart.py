#!/usr/bin/env python

"""
   Usage: combinedchart.py

   This will create a combined chart of all products.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys, shutil
from utils import getProduct, getPotFiles, getPoFilesAsCmdLine

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():

    os.system(__PYTHON + ' create.py combinedchart plone')

    os.chdir('..')
    additional_pots = [p for p in getPotFiles() if p != 'plone.pot']
    shutil.copy('plone.pot', 'combinedchart.pot')
    os.chdir('utils')

    for pot in additional_pots:
        product = getProduct(pot)
        os.system(__PYTHON + ' merge.py combinedchart %s' % product)

    os.system(__PYTHON + ' sync.py combinedchart')

    for pot in additional_pots:
        product = getProduct(pot)
        os.system(__PYTHON + ' admix.py combinedchart %s' % product)

    chart = os.curdir + os.sep + 'charts' + os.sep + 'plone-combined-chart.gif'

    os.chdir('..')
    poFiles = getPoFilesAsCmdLine('combinedchart')
    os.system(__PYTHON + ' ' + __I18NDUDE + (' chart -o %s --pot combinedchart.pot %s') % (chart, poFiles))

if __name__ == '__main__':
    main()
