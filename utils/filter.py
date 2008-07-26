"""
   Usage: filter.py <target-product> <source-product>

   Filter out all msgid's in target product that are already in source product.
"""

import os, sys

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source product.'
        sys.exit(1)

    target = sys.argv[1]+'.pot'
    source = sys.argv[2]+'.pot'

    os.chdir('..')
    os.chdir('i18n')

    if not os.path.isfile(source):
        print 'Source pot was not found for the given product.'
        sys.exit(2)

    if not os.path.isfile(target):
        print 'Target pot was not found for the given product.'
        sys.exit(3)

    os.system(__I18NDUDE + (' filter %s %s > %s-new') % (target, source, target))

if __name__ == '__main__':
    main()
