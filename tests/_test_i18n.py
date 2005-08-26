import os, sys
from Testing import ZopeTestCase
from Products.I18NTestCase import PotTestCase, PoTestCase
from Products.I18NTestCase.I18NTestCase import getPoFiles, getPotFiles, getProductFromPath
from i18ndude import catalog
from Globals import package_home

GLOBALS = globals()
PACKAGE_HOME = os.path.join(package_home(GLOBALS), '..')

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

i18ndir = os.path.join(PACKAGE_HOME, '..', 'i18n')

tests=[]
products=[]
pot_catalogs={}

for potFile in getPotFiles(path=PACKAGE_HOME):
    product = getProductFromPath(potFile)
    if product not in products:
        products.append(product)
    if product not in pot_catalogs:
        pot_catalogs.update({product: catalog.MessageCatalog(filename=potFile, allcomments=True)})

for product in products:
    class TestOnePOT(PotTestCase.PotTestCase):
        pot = product
        path = i18ndir
    tests.append(TestOnePOT)

    for poFile in getPoFiles(path=PACKAGE_HOME, product=product):
        class TestOneMsg(PoTestCase.PotPoTestCase):
            po = poFile
            pot = '%s.pot' % product
            path = i18ndir
        tests.append(TestOneMsg)

        class TestOnePoFile(PoTestCase.PoTestCase):
            po = poFile
            product = product
            pot_cat = pot_catalogs[product]
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

