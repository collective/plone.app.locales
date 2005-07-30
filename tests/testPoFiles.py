import os, re, sys
from glob import glob
import htmlentitydefs
import I18NTestCase

from gettext import GNUTranslations
from Products.PlacelessTranslationService import msgfmt
try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

try:
    import win32api
    WIN32 = True
except ImportError:
    WIN32 = False

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# for testing of untranslated msgstrs
whitelist = ['Netscape Navigator',':','Version 4.x','Internet Explorer',\
             'Version 1.x','Version 6.x','[ ${percentage} %]','${monthname} ${year}',\
             'Version 5.x','Description','Normal Text','Section 508',\
             'SMTP server','Powered by Plone','Valid XHTML','iCal (Mac OS X)',\
             'Zope Management Interface','${type} Details','${fieldset} Details',\
             'vCalendar export','iCalendar export','vCal (Windows, Linux)',\
             'getRawRelatedItems','ExternalEdit','EffectiveDate']

# html entities as they appear in templates
entities = ['&'+ent+';' for ent in htmlentitydefs.entitydefs if ent not in ['hellip','mdash','trade']]

# these are taken from PTS, used for format testing
NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
_interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))


def getFileFromPath(path):
    if WIN32:
        file = path.split('\\')[-1]
    else:
        file = path.split('/')[-1]
    return file

def getLanguageFromPath(path):
    file = getFileFromPath(path)
    # strip of .po
    file = file[:-3]
    lang = file.split('-')[1:]
    return '-'.join(lang)

def getProductFromPath(path):
    file = getFileFromPath(path)
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

    potFiles = [pot for pot in potFiles if not (pot.endswith('manual.pot') or pot.endswith('generated.pot') or pot.endswith('combinedchart.pot'))]

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
    product = None

    def testPoFile(self):
        po = self.poFile
        product = self.product
        poName = getFileFromPath(po)
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

        language = tro._info.get('language-code', None)
        self.failUnless(language, 'Po file %s has no language!' % po)

        fileLang = getLanguageFromPath(po)
        language = language.replace('_', '-')
        self.failUnless(fileLang == language,
            'The file %s has the wrong name or wrong language code. expected: %s, got: %s' % (poName, language, fileLang))

        msgcatalog = tro._catalog

        # testing for proper date_format_* settings
        date_format_long = msgcatalog.get("date_format_long")
        date_format_short = msgcatalog.get("date_format_short")

        if(date_format_long is not None):
            long_number = len(_interp_regex.findall(date_format_long))
            self.failUnless(long_number > 4,
                'Error: Wrong number of date format identifiers in date_format_long in file %s: Expected 5 got %s\n' % (poName, long_number))
        if (date_format_short is not None):
            short_number = len(_interp_regex.findall(date_format_short))
            self.failUnless(short_number > 2,
                'Error: Wrong number of date format identifiers in date_format_short in file %s: Expected 3 got %s\n' % (poName, short_number))

        # the corresponding catalog from products pot
        pot_cat = pot_catalogs.get(product)

        for msg in msgcatalog:
             if msg:
                 msgstr = msgcatalog.get(msg)
                 # every ${foo} is properly closed
                 if '${' in msgstr:
                     self.failUnless(msgstr.count('${') - msgstr.count('}') == 0,
                         'Error: Misformed message attribute ${foo} in file %s:\n %s' % (poName, msg))
                 # no html-entities in msgstr
                 if '&' in msgstr and ';' in msgstr:
                     found = [entity for entity in entities if entity in msgstr]
                     self.failIf(len(found) > 0,
                         'Error: html-entities in file %s:\n %s\n %s' % (poName, msg, found))
                 # check accesskeys for single char
                 if new_i18ndude:
                     orig = pot_cat.get_original(msg)

                     # msgstr is not the same as the original translation
                     if orig:
                         # XXX disable these for now, as they fail with some UnicodeDecodeErrors
                         #orig.replace("+"," ")
                         #self.failIf(orig not in whitelist and len(orig) > 10 and orig.lower() == msgstr.lower(),
                         #    'Warning: msgid is the same as in original english in file %s: %s\n%s' % (poName, msg, orig))

                         # all ${foo}'s from the original should be present in the translation
                         orig_vars = _interp_regex.findall(orig)
                     else:
                         orig_vars = _interp_regex.findall(msg)
                     if orig_vars:
                         orig_vars = [unicode(var) for var in orig_vars]
                         msg_vars = _interp_regex.findall(msgstr)
                         msg_vars = [unicode(var) for var in msg_vars]
                         missing = [var for var in orig_vars if var not in msg_vars]
                         self.failIf(missing,
                             'Warning: Missing message attributes in file %s: %s\n%s' % (poName, msg, missing))

tests=[]

new_i18ndude = True
pot_catalogs={}
for potFile in getPotFiles('..'):
    product = getProductFromPath(potFile)
    if product not in pot_catalogs:
        try:
            pot_catalogs.update({product: catalog.MessageCatalog(filename=potFile, allcomments=True)})
        except TypeError, e:
            if e.args[0].startswith("__init__() got an unexpected keyword argument 'allcomments'"):
                print "You need a newer version (at least 0.5) of i18ndude installed to run all tests."
                new_i18ndude = False
            else:
                raise e

for poFile in getPoFiles('..'):
    product = getProductFromPath(poFile)
    class TestOnePoFile(TestPoFile):
        poFile = poFile
        product = product

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
