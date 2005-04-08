import os, sys
from glob import glob
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import I18NTestCase

from gettext import GNUTranslations
from Products.PlacelessTranslationService import msgfmt

def Xprint(s):
    """print helper
    """
    ZopeTestCase._print(str(s)+'\n')

def getLanguageFromPath(path):
    # get file
    file = path.split('/')[-1]
    # strip of .po
    file = file[:-3]
    lang = file.split('-')[1:]
    return '-'.join(lang)

def getPoFiles(path='..'):
    productPath = os.path.abspath(path)
    i18nPath = os.path.join(productPath, 'i18n')
    if not os.path.isdir(i18nPath):
        # for plone-i18n repository
        i18nPath = productPath
    poFiles= glob(os.path.join(i18nPath, '*.po'))

    if not poFiles:
        raise IOError('No po files found in %s!' % i18nPath)
    return poFiles

class TestPoFile(I18NTestCase.I18NTestCase):
    poFile = None

    def testPoFile(self):
        po = self.poFile
        poName = po.split('/')[-1]
        file = open(po, 'r')
        try:
            lines = file.readlines()
        except IOError, msg:
            self.fail('Can\'t read po file %s:\n%s' % (poName,msg))
        file.close()
        try:
            mo = msgfmt.Msgfmt(lines)
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))
        except SyntaxError, msg:
            self.fail('SyntaxError: Invalid po data syntax in file %s (Can\'t parse file with eval():\n%s' % (poName, msg))
        except Exception, msg:
            self.fail('Unknown error while parsing the po file %s:\n%s' % (poName, msg))
        try:
            tro = GNUTranslations(mo.getAsFile())
        except UnicodeDecodeError, msg:
            self.fail('UnicodeDecodeError in file %s:\n%s' % (poName, msg))
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))

        domain = tro._info.get('domain', None)
        self.failUnless(domain, 'Po file %s has no domain!' % po)

        language_new = tro._info.get('language-code', None) # new way
        language_old = tro._info.get('language', None) # old way
	language = language_new or language_old

	self.failIf(language_old, 'The file %s has the old style language flag set to %s. Please remove it!' % (poName, language_old))
	#if language_old:
	#    self.failUnless(language_new == language_old, 'language and language-code differ in file %s: %s / %s' % (poName, language_new, language_old))

        self.failUnless(language, 'Po file %s has no language!' % po)

        fileLang = getLanguageFromPath(po)
        language = language.lower().replace('_', '-')
        self.failUnless(fileLang == language,
            'The file %s has the wrong name or wrong language code. expected: %s, got: %s' % (poName, language, fileLang))


tests=[]

for poFile in getPoFiles('..'):
    class TestOnePoFile(TestPoFile):
        poFile = poFile

    tests.append(TestOnePoFile)


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
