"""Unit tests for Plone i18n

References:
http://i18n.kde.org/translation-howto/check-gui.html#check-msgfmt
"""

import os, os.path, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import I18NTestCase
import unittest,re
from testPoFiles import getPoFiles, Xprint

from popen2 import popen4

import commands

class TestPOT(I18NTestCase.I18NTestCase):
    def testNoDuplicateMsgId(self):
        """Check that there are no duplicate msgid:s in plone.pot"""
        cmd='grep ^msgid ../plone.pot|sort|uniq --repeated'
        status = commands.getstatusoutput(cmd)
        assert len(status[1])  == 0, "Duplicate msgid:s were found:\n\n%s" % status[1]

class TestMsg(I18NTestCase.I18NTestCase):
    poFile = None

# This test isn't functional yet; msgfmt is pretty useless for automated testing until
# it can present the results in a simple machine-readable way. Now, the message varies
# in formatting depending on the results.
#
#    def testMsgFiles(self):
#        """Check that the .pot file is ok
#
#           "LC_ALL=C" is used so we don't get localised messages from msgfmt."""
#        status = commands.getstatusoutput('LC_ALL=C msgfmt --check --statistics ../plone.pot')
#        if status[0] != 0:
#            self.fail (status[1])


    def testMsgExists(self):
        """
        """
        po = self.poFile
        poName = os.path.split(po)[-1]
        failed=[]
        if not po.endswith("plone-en.po"):
            os.environ['LC_ALL']='C'
            o,i = popen4('msgcmp --directory=.. %s plone.pot' % poName)
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
                self.fail("Comparing plone.pot with %s using msgcmp resulted in:\n%s" % (
                              poName,
                              output))

tests=[]
for poFile in getPoFiles('..'):
    class TestOneMsg(TestMsg):
        poFile = poFile
    tests.append(TestOneMsg)

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
