#!/usr/bin/env python

"""
   Usage: rebuild-pot.py <product> <path to products skins dir>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys, string

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the product und skins directory.'
        sys.exit(1)

    product = sys.argv[1]
    pot = product + '.pot-new'
    manualpot = '%s-manual.pot' % product
    log = 'rebuild-%s-pot.log' % product

    os.chdir('..')

    if not os.path.isfile(manualpot):
        print 'No manual pot was found for the given product.'
        sys.exit(2)

    skins = sys.argv[2]

    if not os.path.isdir(skins):
        print 'Skins directory could not be found.'
        sys.exit(3)

    print 'Rebuilding to %s - this takes a while, logging to %s' % (pot, log)
    os.system(__PYTHON + ' ' + __I18NDUDE + (' rebuild-pot --pot %s --create plone --merge %s -s %s > %s 2>&1') % (pot, manualpot, skins, log))

    # Remove ## X more: occurences
    os.system('sed -r "/## [0-9]+ more:/d" %s > %s2' % (pot, pot))

    # Make paths relative to products skins dir
    os.system('sed -r "s,%s,\.,g" %s2 > %s3' % (string.replace(skins, '\\', '\\\\'), pot, pot))
    os.remove('%s2' % pot)

    # Make directory seperator unix like
    os.system('sed -r "/^#:.*/s,\\\\,/,g" %s3 > %s' % (pot, pot))
    os.remove('%s3' % pot)

if __name__ == '__main__':
    main()
