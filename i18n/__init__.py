import os

try:
    dr = os.path.dirname(__file__)
except AttributeError:
    dr = os.getcwd()

def listLanguages():
    files = []
    for file in os.listdir(dr):
        if file.endswith('.po'):
           files.append(file[6:-3])
    return files

def getFilename(lang):
    return 'plone-%s.po' % lang

def getFile(lang):
    fn = os.path.join(dr, getFilename(lang))
    return open(fn, 'r')

if __name__=='__main__':
    print listLanguages()
