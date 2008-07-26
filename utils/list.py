"""
   Usage: list.py
"""

import os, sys
from utils import getProduct, getPotFiles, getLongProductName
from utils import PRODUCTS

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')

def main():
    option = 'all'
    if len(sys.argv) > 1:
        option = sys.argv[1]

    os.chdir('..')
    os.chdir('i18n')

    products = None
    if option == 'all':
        products = [getProduct(p) for p in getPotFiles()]
    elif option in PRODUCTS.keys():
        products = (getLongProductName(option), )

    if products:
        os.system(__I18NDUDE + (' list --products %s') % (' '.join(products)))

if __name__ == '__main__':
    main()
