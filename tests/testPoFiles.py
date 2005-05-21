import os, re, sys
from glob import glob
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import I18NTestCase
import htmlentitydefs

from gettext import GNUTranslations
from Products.PlacelessTranslationService import msgfmt

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

def Xprint(s):
    """print helper
    """
    ZopeTestCase._print(str(s)+'\n')

def getLanguageFromPath(path):
    # get file
    if WIN32:
        file = path.split('\\')[-1]
    else:
        file = path.split('/')[-1]
    # strip of .po
    file = file[:-3]
    lang = file.split('-')[1:]
    return '-'.join(lang)

def getProductFromPath(path):
    # get file
    if WIN32:
        file = path.split('\\')[-1]
    else:
        file = path.split('/')[-1]
    # strip of .pot
    file = '-'.join(file.split('.')[:1])
    prod = '-'.join(file.split('-')[:1])
    return prod

def getPotFiles(path='..'):
    productPath = os.path.abspath(path)
    i18nPath = os.path.join(productPath, 'i18n')
    if not os.path.isdir(i18nPath):
        # for plone-i18n repository
        i18nPath = productPath
    potFiles= glob(os.path.join(i18nPath, '*.pot'))

    potFiles = [pot for pot in potFiles if not (pot.endswith('manual.pot') or pot.endswith('generated.pot'))]

    if not potFiles:
        raise IOError('No pot files found in %s!' % i18nPath)
    return potFiles

def getPoFiles(path='..', product=''):
    productPath = os.path.abspath(path)
    i18nPath = os.path.join(productPath, 'i18n')
    if not os.path.isdir(i18nPath):
        # for plone-i18n repository
        i18nPath = productPath
    poFiles= glob(os.path.join(i18nPath, '%s*.po' % product))

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
        if language_old:
            self.failUnless(language_new == language_old, 'language and language-code differ in file %s: %s / %s' % (poName, language_new, language_old))

        self.failUnless(language, 'Po file %s has no language!' % po)

        fileLang = getLanguageFromPath(po)
        language = language.replace('_', '-')
        self.failUnless(fileLang == language,
            'The file %s has the wrong name or wrong language code. expected: %s, got: %s' % (poName, language, fileLang))

        # these are taken from PTS
        NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
        _interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))

        msgcatalog = tro._catalog

        # testing for proper date_format_* settings
        date_format_long = msgcatalog.get("date_format_long")
        date_format_short = msgcatalog.get("date_format_short")

        if(date_format_long is not None):
            long_number = len(_interp_regex.findall(date_format_long))
            self.failUnless( long_number == 5,
                'Error: Wrong number of date format identifiers in date_format_long in file %s: Expected 5 got %s\n' % (poName, long_number))
        if (date_format_short is not None):
            short_number = len(_interp_regex.findall(date_format_short))
            self.failUnless(short_number == 3,
                'Error: Wrong number of date format identifiers in date_format_short in file %s: Expected 3 got %s\n' % (poName, short_number))

        for msg in msgcatalog:
             if msg:
                 msgstr = msgcatalog.get(msg)
                 # every ${foo} is properly closed
                 if '${' in msgstr:
                     self.failUnless(msgstr.count('${') - msgstr.count('}') == 0,
                         'Error: Misformed message attribute ${foo} in file %s:\n %s' % (poName, msg))
                 # no html-entities in msgstr
                 if '&' in msgstr and ';' in msgstr:
                     entities = ['&'+ent+';' for ent in htmlentitydefs.entitydefs]
                     found = [entity for entity in entities if entity in msgstr]
                     self.failIf(len(found) > 0,
                         'Error: html-entities in file %s:\n %s\n %s' % (poName, msg, found))

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
