#!/usr/bin/env python

"""
   Usage: rebuild-pot.py <product> <path to products skins dir>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script

   If you are really lazy you can also use atct, atrbw and at as shorthands and if you set your
   INSTANCE_HOME correct, provide '-i' as second argument. This will automagically use the right version.

   So 'rebuilt-pot.py atrbw -i' is a valid shorthand.
"""

import os, sys, string
from utils import getLongProductName

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')
__INSTANCE_HOME = os.environ.get('INSTANCE_HOME', '')

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the product und skins directory.'
        sys.exit(1)

    product = sys.argv[1]

    product = getLongProductName(product)

    pot = product + '.pot-new'
    manualpot = '%s-manual.pot' % product
    generatedpot = '%s-generated.pot' % product
    log = 'rebuild-%s-pot.log' % product

    domain = product

    if product == 'archetypes':
        domain = 'plone'

    os.chdir('..')

    if not os.path.isfile(manualpot):
        print 'Manual pot missing for the given product: %s.' % manualpot
        sys.exit(2)

    skins = sys.argv[2]

    skinserror = False
    if not os.path.isdir(skins):
        if skins == '-i':
            skins = os.path.join(__INSTANCE_HOME, 'Products')
            if os.path.isdir(skins):
                if product == 'atcontenttypes':
                    skins = os.path.join(skins, 'ATContentTypes')
                elif product == 'archetypes':
                    skins = os.path.join(skins, 'Archetypes')
                elif product == 'atreferencebrowserwidget':
                    skins = os.path.join(skins, 'ATReferenceBrowserWidget')
                elif product == 'plone':
                    skins = os.path.join(skins, 'CMFPlone')
                elif product == 'plonelanguagetool':
                    skins = os.path.join(skins, 'PloneLanguageTool')
                elif product == 'linguaplone':
                    skins = os.path.join(skins, 'LinguaPlone')
                skins = os.path.join(skins, 'skins')
            else:
                skinserror = True
        else:
            skinserror = True

    if skinserror:
        print 'Skins directory (%s) could not be found.' % skins
        sys.exit(3)

    print 'Using %s to build new pot.\n' % skins

    cmd = __PYTHON + ' ' + __I18NDUDE + (' rebuild-pot --pot %s --create %s --merge %s ') % (pot, domain, manualpot)

    if product == 'plone' or product == 'atcontenttypes':
        cmd += '--merge2 %s ' % generatedpot

    cmd += '%s > %s 2>&1' % (skins, log)

    print 'Rebuilding to %s - this takes a while, logging to %s' % (pot, log)
    os.system(cmd)

    # Remove ## X more: occurences
    os.system('sed -r "/## [0-9]+ more:/d" %s > %s2' % (pot, pot))

    # Make paths relative to products skins dir
    step3 = pot
    if WIN32:
        step3 = step3 + '3'
    os.system('sed -r "s,%s,\.,g" %s2 > %s' % (string.replace(skins, '\\', '\\\\'), pot, step3))
    os.remove('%s2' % pot)

    if WIN32:
        # Make directory separator unix like
        os.system('sed -r "/^#:.*/s,\\\\,/,g" %s3 > %s' % (pot, pot))
        os.remove('%s3' % pot)

if __name__ == '__main__':
    main()
