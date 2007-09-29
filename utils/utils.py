import os

PRODUCTS = {'atct'  : {'name': 'atcontenttypes', 'path': 'ATContentTypes'},
            'atrbw' : {'name': 'atreferencebrowserwidget', 'path': 'ATReferenceBrowserWidget'},
            'lp'    : {'name': 'linguaplone', 'path': 'LinguaPlone'},
            'plone' : {'name': 'plone', 'path': 'CMFPlone'},
            'plt'   : {'name': 'plonelanguagetool', 'path': 'PloneLanguageTool'},
            'prt'   : {'name': 'passwordresettool', 'path': 'PasswordResetTool'},
            'cmfpw' : {'name': 'cmfplacefulworkflow', 'path': 'CMFPlacefulWorkflow'},
            'cmfe'  : {'name': 'cmfeditions', 'path': 'CMFEditions'},
           }

PRODUCTNAMES = [PRODUCTS[abbr]['name'] for abbr in PRODUCTS]

def getPoFiles(product, all=False):
    """ Returns all product*.po files in the current folder """
    files = os.listdir(os.curdir)
    if all:
        files = [file for file in files if file.startswith('%s-' % product) and file.endswith('.po')]
    else:
        files = [file for file in files if file.startswith('%s-' % product) and file.endswith('.po') and file != '%s-en.po' % product]
    return files


def getPotFiles(all=False):
    """ Returns all pot files in the current folder
        Normally it doesn't return manual.pots and generated.pots
    """
    files = os.listdir(os.curdir)
    if all:
        files = [f for f in files if f.endswith('.pot')]
    else:
        files = [f for f in files if f.endswith('.pot') and not f[:-4].endswith('manual') and not f[:-4].endswith('generated')]
    return files


def getPoFilesAsCmdLine(product):
    files = getPoFiles(product)
    filestring = ''
    for file in files:
        filestring += file + ' '
    return filestring.rstrip()


def getPotFilesAsCmdLine():
    files = getPotFiles()
    filestring = ''
    for file in files:
        filestring += file + ' '
    return filestring.rstrip()


def getPoFilesByLanguageCode(lang):
    """ Returns all po files which ends with given language code."""
    files = os.listdir(os.curdir)
    files = [file for file in files if file.endswith('.po') and file[:-3].endswith(lang)]
    return files


def getLanguage(product, file):
    """ Returns the language part of a po-file """
    lang = None
    if file.endswith('.po'):
        if file.startswith(product):
            lang = '-'.join(file.split('-')[1:])[:-3]
    return lang


def getProduct(file):
    """ Returns the product part of a file. We assume files to be something like domain-language.po.
        Example: atcontenttypes-pt-br.po
    """
    assert file.endswith('.po') or file.endswith('.pot')

    file = file.split('.')[0] # strip of ending
    file = file.split('-')[0] # only take product

    return file

def getLongProductName(product):
    """ Returns the product name for a known abbreviation."""
    if product in PRODUCTS.keys():
        return PRODUCTS[product]['name']
    return product

def getProductPath(product):
    """ Returns the product path for a known abbreviation."""
    if product in PRODUCTS.keys():
        return PRODUCTS[product]['path']
    if product in PRODUCTNAMES:
        for abbr in PRODUCTS.keys():
            if PRODUCTS[abbr]['name'] == product:
                return PRODUCTS[abbr]['path']
    return product

