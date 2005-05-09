import os

try:
    dr = os.path.dirname(__file__)
except AttributeError:
    dr = os.getcwd()

def listLanguages(product='plone'):
    languages = []
    for file in os.listdir(dr):
        if file.endswith('.po'):
            if file.startswith(product):
                lang = '-'.join(file.split('-')[1:])[:-3]
                if lang not in languages:
                    languages.append(lang)
    return languages

def getFilename(lang, product='plone'):
    return '%s-%s.po' % (product, lang)

def getFile(lang, product='plone'):
    fn = os.path.join(dr, getFilename(lang, product=product))
    return open(fn, 'r')

if __name__=='__main__':
    print listLanguages()
