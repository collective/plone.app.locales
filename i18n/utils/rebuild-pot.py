#!/usr/bin/env python

"""
   Usage: rebuild-pot.py <product> <path to products skins dir>
   Note that either 'i18ndude' must be on your path or you have to have set
   I18NDUDE as enviroment variable.

   If you are lazy you can also use atct, atrbw etc. as shorthands and if you
   set your INSTANCE_HOME correctly it will automagically use the right version.

   So 'rebuilt-pot.py atrbw' is a valid shorthand.
   
   At release time, there is also an easy alias 'rebuild-pot.py all' which will
   rebuilt all pot files for all products. You can only use it, if you have
   specified your INSTANCE_HOME.
"""

import os, sys, string
from utils import getLongProductName, getProductPath

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')
__INSTANCE_HOME = os.environ.get('INSTANCE_HOME', '')

def rebuild(product, skins=''):
    product = getLongProductName(product)

    pot = product + '.pot'
    manualpot = '%s-manual.pot' % product
    generatedpot = '%s-generated.pot' % product
    log = 'rebuild-%s-pot.log' % product

    domain = product
    if product == 'archetypes':
        domain = 'plone'

    os.chdir('..')
    if not os.path.isfile(manualpot):
        print 'Manual pot missing for the given product: %s.' % manualpot
        sys.exit(3)

    skinserror = False
    if not os.path.isdir(skins):
        if skins == '':
            skins = os.path.join(__INSTANCE_HOME, 'Products')
            if os.path.isdir(skins):
                skins = os.path.join(skins, getProductPath(product))
                if product not in ['plone', 'cmfplacefulworkflow']:
                    skins = os.path.join(skins, 'skins')
            else:
                skinserror = True
        else:
            skinserror = True

    if skinserror:
        print 'Skins directory (%s) could not be found.' % skins
        sys.exit(4)

    # Remove the original file
    if os.path.isfile(pot):
        os.remove(pot)

    print 'Using %s to build new pot.\n' % skins
    cmd = __I18NDUDE + (' rebuild-pot --pot %s2 --create %s --merge %s ') % (pot, domain, manualpot)
    if product == 'plone' or product == 'atcontenttypes':
        cmd += '--merge2 %s ' % generatedpot
    cmd += '%s > %s 2>&1' % (skins, log)
    print 'Rebuilding to %s - this takes a while, logging to %s' % (pot, log)
    os.system(cmd)

    step2 = pot
    if WIN32:
        step2 = pot + '3'

    # Make paths relative to products skins dir
    os.system('sed "s,%s,\.,g" %s2 > %s' % (string.replace(skins, '\\', '\\\\'), pot, step2))
    os.remove('%s2' % pot)

    if WIN32:
        # Make directory separator unix like
        os.system('sed "/^#:.*/s,\\\\,/,g" %s3 > %s' % (pot, pot))
        os.remove('%s3' % pot)

def main():
    if len(sys.argv) < 2:
        print 'You have to specify an option.'
        sys.exit(1)

    option = sys.argv[1]
    if option == 'all':
        print 'Not yet implemented.'
        sys.exit(2)

    if len(sys.argv) == 2:
        rebuild(sys.argv[1])
    else:
        rebuild(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
