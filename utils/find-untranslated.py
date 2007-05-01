#!/usr/bin/env python

"""
   Usage: find-untranslated.py <product> <path to products skins dir>

   If you are really lazy you can also use atct, atrbw and at as shorthands and if you set your
   INSTANCE_HOME correct, provide '-i' as second argument. This will automagically use the right version.

   So 'find-untranslated.py atrbw -i' is a valid shorthand.
"""

import os, sys, string
from utils import getLongProductName

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')
__INSTANCE_HOME = os.environ.get('INSTANCE_HOME', '')


def main():
    if len(sys.argv) < 3:
        print 'You have to specify the product und skins directory.'
        sys.exit(1)

    product = getLongProductName(sys.argv[1])
    log = 'untranslated-%s.log' % product

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
                skins = os.path.join(skins, 'skins')
            else:
                skinserror = True
        else:
            skinserror = True

    if skinserror:
        print 'Skins directory could not be found.'
        sys.exit(3)

    print 'Looking in %s for untranslated messages' % skins

    os.system(__I18NDUDE + ' find-untranslated -n %s > %s' % (skins, log))

if __name__ == '__main__':
    main()
