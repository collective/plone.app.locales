import os, sys
from Testing import ZopeTestCase
from Products.I18NTestCase import PotTestCase, PoTestCase
from Products.I18NTestCase.I18NTestCase import getPoFiles, getPotFiles, getProductFromPath
from i18ndude import catalog

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

tests=[]
products=[]
pot_catalogs={}

for potFile in getPotFiles():
    product = getProductFromPath(potFile)
    if product not in products:
        products.append(product)
    if product not in pot_catalogs:
        pot_catalogs.update({product: catalog.MessageCatalog(filename=potFile, allcomments=True)})

for product in products:
    class TestOnePOT(PotTestCase.PotTestCase):
        pot = product
    tests.append(TestOnePOT)

    for poFile in getPoFiles(product=product):
        class TestOneMsg(PoTestCase.PotPoTestCase):
            po = poFile
            pot = '%s.pot' % product
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

