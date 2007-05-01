#!/usr/bin/env python

"""
   Usage: merge.py <target-product> <source-product> [<source2-product>]

   Example:

       To keep plone-manual.pot unchanged, copy it to plone-merge.pot. Run:

       merge.py plone-merge plone-manual plone-generated

       You could use plone-merge.pot to mix it in the rebuild-pot process of
       plone.pot.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')


def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source products.'
        sys.exit(1)

    target = sys.argv[1]+'.pot'
    source = sys.argv[2]+'.pot'
    source2 = False
    if len(sys.argv) > 3:
        source2 = sys.argv[3]+'.pot'

    os.chdir('..')

    if not os.path.isfile(source):
        print 'Source pot was not found for the given product.'
        sys.exit(2)

    if not os.path.isfile(target):
        print 'Target pot was not found for the given product.'
        sys.exit(3)

    if source2 and not os.path.isfile(source2):
        print 'Second source pot was not found for the given product.'
        sys.exit(4)

    cmd = __PYTHON + ' ' + __I18NDUDE + (' merge --pot %s --merge %s ') % (target, source)

    if source2:
        cmd += '--merge2 %s ' % source2
    cmd += '-s'
    os.system(cmd)

if __name__ == '__main__':
    main()
