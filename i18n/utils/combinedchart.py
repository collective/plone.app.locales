#!/usr/bin/env python

"""
   Usage: combinedchart.py

   This will create a combined chart of all products.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os
from utils import getPotFiles, getProduct

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():

    os.chdir('..')
    chart = os.curdir + os.sep + 'charts' + os.sep + 'plone-combined-chart.gif'

    pots = getPotFiles()

    products = []
    for pot in pots:
        product = getProduct(pot)
        if not product in products:
            products.append(product)

    products = ' '.join(products)

    os.system(__PYTHON + ' ' + __I18NDUDE + (' combinedchart -o %s --products %s') % (chart, products))

if __name__ == '__main__':
    main()
