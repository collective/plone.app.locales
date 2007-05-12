#!/usr/bin/env python

"""
   Usage: rebuild-pot.py <product> <path to products dir>

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

def rebuild(product, folder=''):
    product = getLongProductName(product)

    pot = product + '.pot'
    manualpot = '%s-manual.pot' % product
    generatedpot = '%s-generated.pot' % product
    log = 'rebuild-%s-pot.log' % product

    domain = product
    if product == 'archetypes':
        domain = 'plone'

    os.chdir('..')
    os.chdir('i18n')

    if not os.path.isfile(manualpot):
        print 'Manual pot missing for the given product: %s.' % manualpot
        sys.exit(3)

    foldererror = False
    if not os.path.isdir(folder):
        if folder == '':
            folder = os.path.join(__INSTANCE_HOME, 'Products')
            if os.path.isdir(folder):
                folder = os.path.join(folder, getProductPath(product))
            else:
                foldererror = True
        else:
            foldererror = True

    if foldererror:
        print 'Product directory (%s) could not be found.' % folder
        sys.exit(4)

    # Remove the original file
    if os.path.isfile(pot):
        os.remove(pot)

    print 'Using %s to build new pot.\n' % folder
    cmd = __I18NDUDE + (' rebuild-pot --pot %s2 --create %s --merge %s ') % (pot, domain, manualpot)
    if product == 'plone':
        cmd += '--merge2 %s ' % generatedpot
    if product == 'plone':
        cmd += '--exclude="rss_template.pt metadata_edit_form.cpt" '
    cmd += '%s > %s 2>&1' % (folder, log)
    print 'Rebuilding to %s - this takes a while, logging to %s' % (pot, log)
    os.system(cmd)

    step2 = pot
    if WIN32:
        step2 = pot + '3'

    # Make paths relative to products skins dir
    os.system('sed "s,%s,\.,g" %s2 > %s' % (string.replace(folder, '\\', '\\\\'), pot, step2))
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
