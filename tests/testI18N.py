"""Unit tests for PloneTranslations

References:
http://i18n.kde.org/translation-howto/check-gui.html#check-msgfmt
"""

import os, os.path, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import I18NTestCase
import unittest,re
from testPoFiles import getPoFiles, getPotFiles, getProductFromPath, Xprint

from popen2 import popen4

import commands

class TestPOT(I18NTestCase.I18NTestCase):
    pot = None

    def testNoDuplicateMsgId(self):
        """Check that there are no duplicate msgid:s in the pot file"""
        pot = self.pot
        cmd='grep ^msgid ../i18n/%s.pot|sort|uniq --repeated' % pot
        status = commands.getstatusoutput(cmd)
        assert len(status[1])  == 0, "Duplicate msgid:s were found:\n\n%s" % status[1]

class TestMsg(I18NTestCase.I18NTestCase):
    poFile = None
    pot = None

    def testMsgExists(self):
        """
        """
        po = self.poFile
        poName = os.path.split(po)[-1]
        pot = self.pot
        poEnglish = '%s-en.po' % pot[:-4]
        failed=[]
        if not po.endswith(poEnglish):
            os.environ['LC_ALL']='C'
            o,i = popen4('msgcmp --directory=../i18n %s %s' % (poName, pot))
            del os.environ['LC_ALL']
            i.close()
            output = o.read()
            o.close()
            if output:
                output = output.split('\n')
                if len(output) > 10:
                    output = output[:10]
                    output.append('... <more errors>')
                output = '\n'.join(output)
                self.fail("Comparing %s with %s using msgcmp resulted in:\n%s" % (
                              pot, poName, output))

tests=[]

products=[]
for potFile in getPotFiles('..'):
    product = getProductFromPath(potFile)
    if product not in products:
        products.append(product)

for product in products:
    for poFile in getPoFiles('..', product=product):
        class TestOneMsg(TestMsg):
            poFile = poFile
            pot = '%s.pot' % product
        tests.append(TestOneMsg)

    class TestOnePOT(TestPOT):
        pot = product
    tests.append(TestOnePOT)


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
