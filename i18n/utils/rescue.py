#!/usr/bin/env python

"""
   Usage: rescue.py

   As we renamed quite some messages in the last time but translators might
   have based their work on an older copy, this script automates this
   renaming process, so it can safely and repeatedly called on all files,
   looking for 'old-style' messages.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys
import getopt
from utils import getPoFiles

try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    os.chdir('..')

    poFiles = getPoFiles('plone')
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(2)

    renamed = {'Exception Log (most recent first)' : 'summary_exception_log',
               'History' : 'summary_history',
               'Returned results' : 'summary_search_results',
               'Review History' : 'summary_review_history',
               'Select roles for each group' : 'summary_roles_for_groups'
              }

    for poFile in poFiles:
        try:
            po_ctl = catalog.MessageCatalog(filename=poFile)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e

        try:
            msgids = po_ctl.keys()
            for old in renamed.keys():
                if old in msgids:
                    new = renamed.get(old)
                    if new in msgids:
                        print 'New message already in %s' % poFile
                    else:
                        po_ctl[new] = po_ctl.get(old)
                        del po_ctl[old]
                        print 'Rename %s to %s in file %s' % (old, new, poFile)
                else:
                    pass
        except IndexError:
            print poFile

        file = open(poFile+'-new', 'w')
        writer = catalog.POWriter(file, po_ctl)
        writer.write(sort=True)

if __name__ == '__main__':
    main()
