#!/usr/bin/env python

"""
   Usage: renamemsgid.py <product> <old_msgid> <new_msgid>

   This is useful to copy a literal msgid over to a new non-literal one with the same translation text.
   Using this is quite nice as not to delete existing translations.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys
import getopt
from utils import getPoFiles, getLongProductName

try:
    import catalog
except:
    from i18ndude import catalog


__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) < 4:
        print 'You have to specify the product and the old and new msgid.'
        sys.exit(1)

    product = getLongProductName(sys.argv[1])

    os.chdir('..')

    poFiles = getPoFiles(product, all=True)
    if poFiles == []:
        print 'No po-files were found for the given product.'
        sys.exit(2)

    old = sys.argv[2]
    new = sys.argv[3]

    for poFile in poFiles:
        try:
            po_ctl = catalog.MessageCatalog(filename=poFile)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e

        try:
            msgids = po_ctl.keys()
            if old in msgids:
                if new in msgids:
                    print 'New message already in %s' % poFile
                else:
                    po_ctl[new] = po_ctl.get(old)
                    del po_ctl[old]
                    print 'Rename %s to %s in file %s' % (old, new, poFile)
            else:
                print 'Old message not found in %s' % poFile
        except IndexError:
            print poFile

        file = open(poFile+'-new', 'w')
        writer = catalog.POWriter(file, po_ctl)
        writer.write(sort=True)

if __name__ == '__main__':
    main()
