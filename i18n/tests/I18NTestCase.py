#
# PloneTestCase
#

# $Id: I18NTestCase.py,v 1.1 2004/01/28 12:47:50 tiran Exp $

from Testing import ZopeTestCase

ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)
#ZopeTestCase.installProduct('PlacelessTranslationService')
#ZopeTestCase.installProduct('CMFCore')
#ZopeTestCase.installProduct('CMFDefault')
#ZopeTestCase.installProduct('CMFCalendar')
#ZopeTestCase.installProduct('CMFTopic')
#ZopeTestCase.installProduct('DCWorkflow')
#ZopeTestCase.installProduct('CMFActionIcons')
#ZopeTestCase.installProduct('CMFQuickInstallerTool')
#ZopeTestCase.installProduct('CMFFormController')
#ZopeTestCase.installProduct('Formulator')
#ZopeTestCase.installProduct('GroupUserFolder')
#ZopeTestCase.installProduct('ZCTextIndex')
#ZopeTestCase.installProduct('CMFPlone')
#ZopeTestCase.installProduct('MailHost', quiet=1)

class I18NTestCase(ZopeTestCase.ZopeTestCase):
    pass

