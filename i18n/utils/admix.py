#!/usr/bin/env python

"""
   Usage: admix.py <target-product> <source-product>
   Note that PYTHON and I18NDUDE must have been set as enviroment variables before calling this script
"""

import os, sys

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def getPoFiles(product):
    files = os.listdir(os.curdir)
    files = [file for file in files if file.startswith(product) and file.endswith('.po') and file != '%s-en.po' % product]
    return files

def getLanguage(product, file):
    lang = None
    if file.endswith('.po'):
        if file.startswith(product):
            lang = '-'.join(file.split('-')[1:])[:-3]
    return lang

def main():
    if len(sys.argv) < 3:
        print 'You have to specify the target and source product.'
        sys.exit(1)

    target = sys.argv[1]
    source = sys.argv[2]

    os.chdir('..')

    targetPoFiles = getPoFiles(target)
    sourcePoFiles = getPoFiles(source)

    if targetPoFiles == '' or sourcePoFiles == '':
        print 'No po-files were found for one of the given products.'
        sys.exit(3)

    for t in targetPoFiles:
        targetLanguage = getLanguage(target,t)
        for s in sourcePoFiles:
            sourceLanguage = getLanguage(source,s)
            if targetLanguage and sourceLanguage and targetLanguage == sourceLanguage:
                print '%s %s <- %s' % (getLanguage(target, t), t, s)
                os.system(__PYTHON + ' ' + __I18NDUDE + (' admix %s %s > %s') % (t, s, t))

if __name__ == '__main__':
    main()
