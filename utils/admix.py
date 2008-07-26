"""
   Usage: admix.py <target-product> <source-product>
"""

import os, sys, shutil
from utils import getPoFiles, getLanguage

__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source product.'
        sys.exit(1)

    target = sys.argv[1]
    source = sys.argv[2]

    os.chdir('..')
    os.chdir('i18n')

    targetPoFiles = getPoFiles(target)
    sourcePoFiles = getPoFiles(source)

    if targetPoFiles == [] or sourcePoFiles == []:
        print 'No po-files were found for one of the given products.'
        sys.exit(3)

    for t in targetPoFiles:
        targetLanguage = getLanguage(target,t)
        for s in sourcePoFiles:
            sourceLanguage = getLanguage(source,s)
            if targetLanguage and sourceLanguage and targetLanguage == sourceLanguage:
                print '%s %s <- %s' % (getLanguage(target, t), t, s)
                os.system(__I18NDUDE + (' admix %s %s > %s-new') % (t, s, t))
                targetpath = os.path.join(os.curdir, t)
                os.remove(targetpath)
                if not os.path.exists(targetpath):
                    shutil.copy(t+'-new', t)
                    os.remove(targetpath+'-new')

if __name__ == '__main__':
    main()
