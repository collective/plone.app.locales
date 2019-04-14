# -*- coding: utf-8 -*-
"""
   Usage: setcomment.py <product> <comment>
"""

from __future__ import print_function
from utils import getPoFiles, getLongProductName
import os, sys

from i18ndude import catalog


def main():
    if len(sys.argv) < 2:
        print('You have to specify the product.')
        sys.exit(1)

    product = getLongProductName(sys.argv[1])

    os.chdir('..')
    os.chdir('i18n')

    poFiles = getPoFiles(product, all=True)
    if poFiles == []:
        print('No po-files were found for the given product.')
        sys.exit(2)

    for poFile in poFiles:
        try:
            po_ctl = catalog.MessageCatalog(filename=poFile)
        except IOError as e:
            print('I/O Error: %s' % e, file=sys.stderr)

        try:
            language = po_ctl.commentary_header[0].split('to ')[1:][0]
            po_ctl.commentary_header[0] = 'Translation of '+product+'.pot to '+language
        except IndexError:
            print(poFile)

        file = open(poFile+'-new', 'w')
        writer = catalog.POWriter(file, po_ctl)
        writer.write(sort=False)

if __name__ == '__main__':
    main()
