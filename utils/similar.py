#!/usr/bin/env python

"""
   Usage: similar.py <potfile>

   Looks for msgid's in a pot file that are very similar. Meaning only case
   and whitespace differences.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys
import getopt

try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():

    if len(sys.argv) < 2:
        print 'You have to specify the pot file.'
        sys.exit(1)

    pot = sys.argv[1]

    os.chdir('..')

    try:
        po_ctl = catalog.MessageCatalog(filename=pot)
    except IOError, e:
        print >> sys.stderr, 'I/O Error: %s' % e

    similar = {}
    try:
        for msgid in po_ctl.keys():
            norm = msgid.strip().lower().replace(' ','')
            if similar.get(norm):
                similar[norm].append(msgid)
            else:
                similar[norm] = [msgid]

        for k in similar:
            v = similar.get(k)
            if len(v) > 1:
                print k, v

    except IndexError:
            print poFile

if __name__ == '__main__':
    main()
