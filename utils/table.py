"""
Usage: table.py
"""

from utils import getLongProductName
from utils import getPotFiles
from utils import getProduct
from utils import PRODUCTS

import os
import sys


__I18NDUDE = os.environ.get("I18NDUDE", "i18ndude")


def main():
    option = "all"
    if len(sys.argv) > 1:
        option = sys.argv[1]

    os.chdir("..")
    os.chdir("i18n")

    products = None
    if option == "all":
        products = [getProduct(p) for p in getPotFiles()]
    elif option in list(PRODUCTS.keys()):
        products = (getLongProductName(option),)

    if products:
        os.system(__I18NDUDE + (" list -t --products %s") % (" ".join(products)))


if __name__ == "__main__":
    main()
