import os

PRODUCTS = {
    'atct'  : {'name': 'atcontenttypes', 'path': 'ATContentTypes'},
    'atrbw' : {'name': 'atreferencebrowserwidget', 'path': 'ATReferenceBrowserWidget'},
    'lp'    : {'name': 'linguaplone', 'path': 'LinguaPlone'},
    'plone' : {'name': 'plone', 'path': 'CMFPlone'},
    'plt'   : {'name': 'plonelanguagetool', 'path': 'PloneLanguageTool'},
    'prt'   : {'name': 'passwordresettool', 'path': 'PasswordResetTool'},
    'cmfpw' : {'name': 'cmfplacefulworkflow', 'path': 'CMFPlacefulWorkflow'},
    'cmfe'  : {'name': 'cmfeditions', 'path': 'CMFEditions'},
    'kupu'  : {'name': 'kupu/kupu', 'path': 'kupu'},
    'kupuconfig'  : {'name': 'kupu/kupuconfig', 'path': 'kupu'},
    'kupupox'  : {'name': 'kupu/kupupox', 'path': 'kupu'},
    }

PRODUCTNAMES = [PRODUCTS[abbr]['name'] for abbr in PRODUCTS]

def getPoFiles(product, all=False):
    """ Returns all product*.po files in the current folder """
    path = os.curdir
    folder = ''
    if '/' in product:
        folder, product = product.split('/')
        path = os.path.join(os.curdir, folder)

    files = os.listdir(path)
    if all:
        files = [f for f in files if f.startswith('%s-' % product) and f.endswith('.po')]
    else:
        files = [f for f in files if f.startswith('%s-' % product) and f.endswith('.po') and f != '%s-en.po' % product]
    if folder:
        files  = [folder + '/' + f for f in files]
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
    for f in files:
        filestring += f + ' '
    return filestring.rstrip()


def getPotFilesAsCmdLine():
    files = getPotFiles()
    filestring = ''
    for f in files:
        filestring += f + ' '
    return filestring.rstrip()


def getPoFilesByLanguageCode(lang):
    """ Returns all po files which ends with given language code."""
    files = os.listdir(os.curdir)
    files = [f for f in files if f.endswith('.po') and f[:-3].endswith(lang)]
    return files


def getLanguage(product, f):
    """ Returns the language part of a po-file """
    lang = None
    if f.endswith('.po'):
        if f.startswith(product):
            lang = '-'.join(f.split('-')[1:])[:-3]
    return lang


def getProduct(f):
    """ Returns the product part of a file. We assume files to be something like domain-language.po.
        Example: atcontenttypes-pt-br.po
    """
    assert f.endswith('.po') or f.endswith('.pot')

    f = f.split('.')[0] # strip of ending
    f = f.split('-')[0] # only take product

    return f


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
