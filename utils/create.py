"""
   Usage: create.py <target-product> <source-product>

   Creates copies of all existing po files of the source product under the name of the target product.
   This is useful to preserves headers of the files and to give a starting point for work.

   You have to run merge after that, to remove the wrong msgid's and include the one's from the actual product

   Using admix.py can then copy over existing translations.
"""

import os, sys, shutil
from utils import getPoFiles, getLanguage


def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source product.'
        sys.exit(1)

    target = sys.argv[1]
    source = sys.argv[2]

    os.chdir('..')

    sourcePoFiles = getPoFiles(source)

    if sourcePoFiles == []:
        print 'No po-files were found for the source product.'
        sys.exit(3)

    for sourcefile in sourcePoFiles:
        sourceLanguage = getLanguage(source,sourcefile)
        if sourceLanguage:
            targetfile = target + '-' + sourceLanguage + '.po'
            targetpath = os.path.join(os.curdir, targetfile)
            if not os.path.exists(targetpath):
                shutil.copy(sourcefile, targetfile)

if __name__ == '__main__':
    main()
