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
from Products.Archetypes.Schema import getSchemata
from Products.Archetypes.Field import ReferenceField
from Products.Archetypes.utils import DisplayList
from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation

try:
    from Products.i18ndude import catalog
    from Products.i18ndude.catalog import MAX_OCCUR
except ImportError:
    from i18ndude import catalog
    from i18ndude.catalog import MAX_OCCUR

from Products.CMFPlone.i18nl10n import monthname_english, weekdayname_english, \
     monthname_msgid, monthname_msgid_abbr, weekdayname_msgid, \
     weekdayname_msgid_abbr, weekdayname_msgid_short

class TestI18N(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.action_tool = self.portal.portal_actions
        self.wf_tool = self.portal.portal_workflow
        self.types_tool = self.portal.portal_types
        self.at_tool = self.portal.archetype_tool
        self.atct_tool = self.portal.portal_atct
        self.ai_tool = self.portal.portal_actionicons
        self.cp_tool = self.portal.portal_controlpanel

    def testI18Ngenerator(self):
        '''Runs the i18ngenerator'''

        ctl = {}
        ctl['plone'] = catalog.MessageCatalog(domain='plone')

        # global actions
        for provider in self.action_tool.listActionProviders():
            provider_tool = getToolByName(self.portal, provider, None)
            for action in provider_tool.listActions():
                title = norm(action.title)
                if action.visible:
                    ctl['plone'].add(title, msgstr=title, filename='action', excerpt=['defined in %s' %provider])

        # description of action icons
        for icon in self.ai_tool.listActionIcons():
            title= icon.getTitle()
            ctl['plone'].add(title, msgstr=title, filename='action_icon', excerpt=['id: %s, category: %s' % (icon.getIconURL(), icon.getCategory())])


        # workflow states and worflow transitions
        for workflow in self.wf_tool.listWorkflows():
            wf = self.wf_tool.getWorkflowById(workflow)
            for obj in wf.objectValues():
                if isinstance(obj, States.States):
                    for state in obj.objectValues():
                        ctl['plone'].add(state.getId(), msgstr=state.getId(), filename='workflow_state', excerpt=['defined in %s, title: %s' % (workflow, state.title)])
                        ctl['plone'].add(state.title, msgstr=state.title, filename='workflow_state', excerpt=['defined in %s, id: %s' % (workflow, state.getId())])
                elif isinstance(obj, Transitions.Transitions):
                    for transition in obj.objectValues():
                        ctl['plone'].add(transition.getId(), msgstr=transition.getId(), filename='workflow_transition', excerpt=['defined in %s, title: %s' % (workflow, transition.title), 'new state: %s' % transition.new_state_id])
                        ctl['plone'].add(transition.title, msgstr=transition.title, filename='workflow_transition', excerpt=['defined in %s, id: %s' % (workflow, transition.getId()), 'new state: %s' % transition.new_state_id])
                        ctl['plone'].add(transition.actbox_name, msgstr=transition.actbox_name, filename='workflow_action', excerpt=['defined in %s, title: %s' % (workflow, transition.title), 'new state: %s' % transition.new_state_id])


        # portal types and types actions
        types = [t for t in self.types_tool.listContentTypes() if not t.startswith('CMF ')] # filter out CMF types

        for type in types:
            typeObj = self.types_tool.getTypeInfo(type)

            methods = []
            try:
                methods = typeObj.view_methods
            except AttributeError:
                # this type doesn't support the DynamicViewFTI
                pass

            for method in methods:
                mid = getattr(typeObj, method, None)
                title = mid.aq_inner.aq_explicit.title_or_id()
                if type.endswith('Folder') or type == 'Topic': # XXX Need a better way to filter out unused views
                    ctl['plone'].addToSameFileName(title, msgstr=title, filename='dynamic view name', excerpt=['template %s on type: %s' % (method, type)])

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
        for group in self.cp_tool.getGroups():
            id = group.get('id')
            title = group.get('title')
            ctl['plone'].add(title, msgstr=title, filename='controlpanel_category', excerpt=['category-id: %s' % id])

        # day and monthnames
        for num in range(7):
            day = weekdayname_english(num) # Monday, Tuesday...
            ctl['plone'].add(weekdayname_msgid(num), msgstr=day, filename='datetime', excerpt=['name of a day, format %A'])
            day = weekdayname_english(num, 'a') # Mon, Tue, ...
            ctl['plone'].add(weekdayname_msgid_abbr(num), msgstr=day, filename='datetime', excerpt=['abbreviation of a day, format %a'])
            day = weekdayname_english(num, 'a')[:2] # Mo, Tu, ...
            ctl['plone'].add(weekdayname_msgid_short(num), msgstr=day, filename='datetime', excerpt=['two letter abbreviation of a day used in the portlet_calendar'])
        for num in range(1,13):
            month = monthname_english(num) # January, February...
            ctl['plone'].add(monthname_msgid(num), msgstr=month, filename='datetime', excerpt=['name of a month, format %B'])
            month = monthname_english(num, 'a') # Jan, Feb...
            ctl['plone'].add(monthname_msgid_abbr(num), msgstr=month, filename='datetime', excerpt=['name of a month, format %b'])

        # indexes and metadata and smart folder options
        domain = 'plone'
        for index in self.atct_tool.getIndexes(enabledOnly=1):
            index = self.atct_tool.getIndex(index)
            id = index.index
            title = index.friendlyName
            desc = index.description
            ctl[domain].addToSameFileName(id, msgstr=id, filename='index', excerpt=['index id with index friendly name: %s' % title])
            if title:
                ctl[domain].addToSameFileName(title, msgstr=title, filename='index', excerpt=['index friendly name of index: %s' % id])
            if desc:
                ctl[domain].addToSameFileName(desc, msgstr=desc, filename='index', excerpt=['index description of index: %s' % id])
            # add in criterions
            for criterion in self.atct_tool.getCriteriaForIndex(id, as_dict= True):
                name = criterion['name']
                desc = criterion['description']
                ctl[domain].addToSameFileName(desc, msgstr=desc, filename='criteria', excerpt=['criterion description of crterion: %s' % name])
        for meta in self.atct_tool.getAllMetadata(enabledOnly=1):
            meta = self.atct_tool.getMetadata(meta)
            id = meta.index
            title = meta.friendlyName
            desc = meta.description
            ctl[domain].addToSameFileName(id, msgstr=id, filename='metadata', excerpt=['metadata id with metadata friendly name: %s' % title])
            if title:
                ctl[domain].addToSameFileName(title, msgstr=title, filename='metadata', excerpt=['metadata friendly name of metadata: %s' % id])
            if desc:
                ctl[domain].addToSameFileName(desc, msgstr=desc, filename='metadata', excerpt=['metadata description of metadata: %s' % id])

        # DisplayList properties XXX This takes only static DisplayLists for now. Need to look at dynamically generated ones (which need a content object to be present)

        for attype in self.at_tool.listRegisteredTypes():
            schema = attype['schema']
            for field in schema.fields():
                if not isinstance(field, ReferenceField):
                    domain = field.widget.__dict__.get('i18n_domain')
                    vocab = field.Vocabulary()
                    if isinstance(vocab, DisplayList):
                        for key in vocab:
                            value = vocab.getValue(key)
                            if len(value) > 1:
                                msgid = vocab.getMsgId(key)
                                if domain == None:
                                    domain = 'plone'
                                if not domain in ctl.keys():
                                    ctl[domain] = catalog.MessageCatalog(domain=domain)
                                ctl[domain].addToSameFileName(msgid, msgstr=value, filename='schema', excerpt=['DisplayList entry for field %s' % field.getName()])


        # archetypes widgets XXX Should be merged with the DisplayList stuff

        for widget in self.at_tool.getWidgets():
            w = widget._args.get('widget')
            dict = w.__dict__
            domain = dict.get('i18n_domain')
            if domain:
                if not domain in ctl.keys():
                    ctl[domain] = catalog.MessageCatalog(domain=domain)
                label = dict.get('label')
                label_msgid = dict.get('label_msgid')
                desc = norm(dict.get('description'))
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
