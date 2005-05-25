#!/usr/bin/env python

"""
   Usage: setprojid.py <product> <projectid>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys
import getopt

try:
    import common, untranslated, catalog, visualisation
except:
    from i18ndude import common, untranslated, catalog, visualisation


__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def getPoFiles(product):
    files = os.listdir(os.curdir)
    files = [file for file in files if file.startswith(product) and file.endswith('.po')]
    return files

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the product and the new text for projectid.'
        sys.exit(1)

    product = sys.argv[1]
    projectid = sys.argv[2]

    os.chdir('..')

    poFiles = getPoFiles(product)
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(2)

    for poFile in poFiles:
        try:
            po_ctl = catalog.MessageCatalog(filename=poFile)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e
        po_ctl.mime_header['Project-Id-Version'] = projectid
        file = open(poFile, 'w')
        writer = catalog.POWriter(file, po_ctl)
        writer.write(sort=False)

if __name__ == '__main__':
    main()
