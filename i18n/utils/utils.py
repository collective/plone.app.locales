import os

def getPoFiles(product, all=False):
    """ Returns all product*.po files in the current folder """
    files = os.listdir(os.curdir)
    if all:
        files = [file for file in files if file.startswith(product) and file.endswith('.po')]
    else:
        files = [file for file in files if file.startswith(product) and file.endswith('.po') and file != '%s-en.po' % product]
    return files

def getPoFilesAsCmdLine(product):
    files = getPoFiles(product)
    filestring = ''
    for file in files:
        filestring += file + ' '
    return filestring.rstrip()

def getLanguage(product, file):
    """ Returns the language part of a po-file """
    lang = None
    if file.endswith('.po'):
        if file.startswith(product):
            lang = '-'.join(file.split('-')[1:])[:-3]
    return lang

