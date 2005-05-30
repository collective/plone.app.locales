#
# To run the i18ngenerator in this instance type
#
#   $ python i18ngenerator.py
#
# This is a fake test that uses PloneTestCase to start a standarized Plone
# instance and collects all kinds of strings needing translation, building
# <domain>-generated.pot's.
#
# Currently it searches for actions definied on all action providers, type
# names, descriptions and actions definied on types, workflow states and
# transitions and puts these into a plone-generated.pot.
#
# In a second step it searches for all widgets registered with the
# archetype_tool and collects all labels and descriptions (including msgids)
# and puts these into seperate files for their definied i18n_domain.
#
# For now this generates a atcontenttypes-generated.pot in addition to the
# plone-generated.pot.
#
# These pot's should contain much of the strings currently in the
# <domain>-manual.pot's and can be used instead. As they are automatically
# build there should be much less outdated msgids.
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow import States, Transitions

try:
    from Products.i18ndude import catalog
    from Products.i18ndude.catalog import MAX_OCCUR
except ImportError:
    from i18ndude import catalog
    from i18ndude.catalog import MAX_OCCUR

KNOWS_CALENDAR_NAMES = True
try:
    from Products.CMFPlone.i18nl10n import monthname_english, weekdayname_english
except ImportError:
    KNOWS_CALENDAR_NAMES = False
    print "Error importing i18nl10n.py -> no automatic day/monthname generation"

class TestI18N(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.action_tool = self.portal.portal_actions
        self.wf_tool = self.portal.portal_workflow
        self.types_tool = self.portal.portal_types
        try:
            self.at_tool = self.portal.archetype_tool
        except AttributeError:
            self.at_tool = False
        try:
            self.ai_tool = self.portal.portal_actionicons
        except AttributeError:
            self.ai_tool = False
        try:
            self.cp_tool = self.portal.portal_controlpanel
        except AttributeError:
            self.cp_tool = False

    def testI18Ngenerator(self):
        '''Runs the i18ngenerator'''

        ctl = {}
        ctl['plone'] = catalog.MessageCatalog(domain='plone')

        # global actions
        action_providers = [tool for tool in self.action_tool.listActionProviders() if tool != 'portal_workflow']

        for provider in action_providers:
            provider_tool = getToolByName(self.portal, provider, None)
            for action in provider_tool.listActions():
                title = norm(action.title)
                ctl['plone'].add(title, msgstr=title, filename='action', excerpt=['defined in %s' %provider])


        # description of action icons
        if self.ai_tool:
            action_icons = self.ai_tool.listActionIcons()
        else:
            action_icons = []
        for icon in action_icons:
            title= icon.getTitle()
            ctl['plone'].add(title, msgstr=title, filename='action_icon', excerpt=['id: %s, category: %s' % (icon.getIconURL(), icon.getCategory())])


        # workflow states and worflow transitions
        workflows = self.wf_tool.listWorkflows()

        for workflow in workflows:
            wf = self.wf_tool.getWorkflowById(workflow)
            for obj in wf.objectValues():
                if isinstance(obj, States.States):
                    for state in obj.objectValues():
                        ctl['plone'].add(state.getId(), msgstr=state.getId(), filename='workflow_state', excerpt=['defined in %s, title: %s' % (workflow, state.title)])
                elif isinstance(obj, Transitions.Transitions):
                    for transition in obj.objectValues():
                        ctl['plone'].add(transition.getId(), msgstr=transition.getId(), filename='workflow_transition', excerpt=['defined in %s, title: %s' % (workflow, transition.title), 'new state: %s' % transition.new_state_id])


        # portal types and types actions
        types = [t for t in self.types_tool.listContentTypes() if not t.startswith('CMF ')] # filter out CMF types

        for type in types:
            typeObj = self.types_tool.getTypeInfo(type)
            title = norm(typeObj.Title())
            desc = norm(typeObj.Description())
            ctl['plone'].add(title, msgstr=title, filename='portal_type_title', excerpt=['type description: %s' % desc])
            ctl['plone'].add(desc, msgstr=desc, filename='portal_type_description', excerpt=['type title: %s' % title])

            # don't show actions definied on criteria
            if title.lower().find('criteri') == -1:
                for action in typeObj.listActions():
                    actionTitle = norm(action.title)
                    ctl['plone'].addToSameFileName(actionTitle, msgstr=actionTitle, filename='type_action', excerpt=['defined on %s' % title])

        # portal_controlpanel categories
        if self.cp_tool:
            groups = self.cp_tool.getGroups()
        else:
            groups = []
        for group in groups:
            id = group.get('id')
            title = group.get('title')
            ctl['plone'].add(title, msgstr=title, filename='controlpanel_category', excerpt=['category-id: %s' % id])

        # day and monthnames
        if KNOWS_CALENDAR_NAMES:
            for num in range(6):
                day = weekdayname_english(num) # Monday, Tuesday...
                ctl['plone'].add(day, msgstr=day, filename='datetime', excerpt=['name of a day, format %A'])
                day = weekdayname_english(num, 'a') # Mon, Tue, ...
                ctl['plone'].add(day, msgstr=day, filename='datetime', excerpt=['abbreviation of a day, format %a'])
                day = weekdayname_english(num, 'a')[:2] # Mo, Tu, ...
                ctl['plone'].add(day, msgstr=day, filename='datetime', excerpt=['two letter abbreviation of a day used in the portlet_calendar'])
            for num in range(1,13):
                month = monthname_english(num) # January, February...
                ctl['plone'].add(month, msgstr=month, filename='datetime', excerpt=['name of a month, format %B'])
                month = monthname_english(num, 'a') # Jan, Feb...
                ctl['plone'].add(month, msgstr=month, filename='datetime', excerpt=['name of a month, format %b'])

        # archetypes widgets
        if self.at_tool:
            widgets = self.at_tool.getWidgets()
        else:
            widgets = []

        for widget in widgets:
            w = widget._args.get('widget')
            dict = w.__dict__
            domain = dict.get('i18n_domain')
            if domain:
                if not domain in ctl.keys():
                    ctl[domain] = catalog.MessageCatalog(domain=domain)
                label = dict.get('label')
                label_msgid = dict.get('label_msgid')
                desc = dict.get('description')
                desc_msgid = dict.get('description_msgid')

                if label_msgid and label:
                    ctl[domain].add(label_msgid, label, filename='widget_label', excerpt=['of %s, description: %s' % (w.getName(), desc)])
                if desc_msgid and desc:
                    ctl[domain].add(desc_msgid, desc, filename='widget_description', excerpt=['of %s, for label: %s' % (w.getName(), label)])

        domains = ctl.keys()

        for domain in domains:
            file = open('%s-generated.pot' % domain, 'w')
            writer = catalog.POWriter(file, ctl[domain])
            writer.write(sort=True, msgstrToComment=True, noMoreComments=True)

def norm(str):
    return str.strip().replace('\n','')

if __name__ == '__main__':
    framework(verbosity=0)
