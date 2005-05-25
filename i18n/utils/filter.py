#!/usr/bin/env python

"""
   Usage: filter.py <target-product> <source-product>

   Filter out all msgid's in target product that are already in source product.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source product.'
        sys.exit(1)

    target = sys.argv[1]+'.pot'
    source = sys.argv[2]+'.pot'

    os.chdir('..')

    if not os.path.isfile(source):
        print 'Source pot was not found for the given product.'
        sys.exit(2)

    if not os.path.isfile(target):
        print 'Target pot was not found for the given product.'
        sys.exit(3)

    os.system(__PYTHON + ' ' + __I18NDUDE + (' filter %s %s > %s-new') % (target, source, target))

if __name__ == '__main__':
    main()
