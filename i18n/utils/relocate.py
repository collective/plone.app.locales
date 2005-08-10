#!/usr/bin/env python

"""
   Usage: relocate.py

   As we moved quite some messages between domains lately, this script
   automates this process, so it can be repeatedly and safely called on po
   files to preserve translations.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys
import getopt
from utils import getPoFiles, getLanguage

try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    os.chdir('..')

    poFilesPlone = getPoFiles('plone')
    if not poFilesPlone:
        print 'No po-files were found for Plone.'
        sys.exit(2)

    poFilesATCT = getPoFiles('atcontenttypes')
    if not poFilesATCT:
        print 'No po-files were found for ATContentTypes.'
        sys.exit(3)

    # format: 'old-domain' : ['msgid1', 'msgid2', ...]
    # currently only relocating between atcontenttypes and plone and vica versa is possibly
    relocated = {'atcontenttypes' :
                  ['A boolean criterion', 'A date criteria',
                   'A date range criterion', 'A list criterion', 'A path criterion',
                   'A portal_types criterion', 'A reference criterion', 'A selection criterion',
                   'A simple int criterion', 'A simple string criterion', 'help_limit_number',
                   'A criterion that searches for the currently logged in user\'s id',
                   'help_event_attendees', 'help_item_count',
                   'help_string_criteria_value', 'label_event_attendees',
                   'label_item_count', 'label_limit_number',
                   'label_string_criteria_value',
                   'An item\'s title transformed for sorting', 'An item\'s type (e.g. Event)',
                   'An item\'s workflow state (e.g.published)', 'Boolean (True/False)',
                   'Creation Date', 'CreationDate', 'Creator', 'Date range', 'Description',
                   'Effective Date', 'EffectiveDate', 'End Date', 'Expiration Date',
                   'ExpirationDate', 'Find items related to the selected items',
                   'Integer value or range', 'Item Type', 'List of values', 'Location',
                   'Location in portal', 'Modification Date', 'ModificationDate',
                   'Related To', 'Relative date', 'Restrict to current user',
                   'Search Text', 'SearchableText', 'Select content types',
                   'Select referenced content', 'Select values from list', 'Short Name',
                   'Size', 'Start Date', 'State', 'Subject', 'Text', 'start',
                   'Text search of an item\'s contents', 'Text search of an item\'s title',
                   'The end date and time of an event', 'The location an item in the portal (path)',
                   'The short name of an item (used in the url)', 'The size of an item',
                   'The start date and time of an event', 'The time and date an item becomes publicly available',
                   'The time and date an item is no longer publically available',
                   'The time and date an item is no longer publicly available',
                   'The time and date an item was created', 'The time and date an item was last modified',
                   'Title', 'Type', 'created', 'effective', 'end', 'expires', 'getId', 'getObjSize',
                   'getRawRelatedItems', 'location', 'modified', 'path', 'review_state', 'sortable_title'
                  ],
                 'plone' :
                  ['help_int_criteria_direction', 'help_int_criteria_value2',
                   'label_int_criteria_direction', 'label_int_criteria_value2'
                  ]
                }

    # make sure we only try on languages for which both po files exist
    ploneLanguages = [getLanguage('plone', p) for p in poFilesPlone]
    atctLanguages = [getLanguage('atcontenttypes', p) for p in poFilesATCT]

    languages = [l for l in ploneLanguages if l in atctLanguages and l != 'en']
    changes = {'plone' : False, 'atcontenttypes' : False}

    for lang in languages:
        po_ctl = {}
        try:
            po_ctl['plone'] = catalog.MessageCatalog(filename='plone-%s.po' % lang)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e
        try:
            po_ctl['atcontenttypes'] = catalog.MessageCatalog(filename='atcontenttypes-%s.po' % lang)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e

        changes = {'plone' : False, 'atcontenttypes' : False}

        relocate_domain = {'plone' : 'atcontenttypes', 'atcontenttypes' : 'plone'}

        msgids = {}
        msgids['plone'] = po_ctl['plone'].keys()
        msgids['atcontenttypes'] = po_ctl['atcontenttypes'].keys()

        for old_domain in relocated:
            relocate_msgids = relocated.get(old_domain)
            for relocate_msgid in relocate_msgids:
                if relocate_msgid in msgids[old_domain]:
                    msgstr = po_ctl[old_domain].get(relocate_msgid)
                    del po_ctl[old_domain][relocate_msgid]
                    changes[old_domain] = True

                    new_domain = relocate_domain.get(old_domain)
                    if relocate_msgid in msgids[new_domain]:
                        old_msgstr = po_ctl[new_domain].get(relocate_msgid)
                        print old_msgstr[0], 'bla ', msgstr
                        if old_msgstr[0] == '' and msgstr:
                            po_ctl[new_domain][relocate_msgid] = msgstr
                            changes[new_domain] = True
                            print 'copied msgstr for %s' % relocate_msgid
                        #else:
                        #    print '%s was already there' % relocate_msgid
                    else:
                        po_ctl[new_domain][relocate_msgid] = msgstr
                        changes[new_domain] = True
                        print 'copied %s to %s-%s.po' % (relocate_msgid, new_domain, lang)
                #else:
                #    print '%s was not found anymore' % relocate_msgid

        for domain in changes:
            if changes[domain]:
                file = open('%s-%s.po-new' % (domain, lang), 'w')
                writer = catalog.POWriter(file, po_ctl[domain])
                writer.write(sort=True)

if __name__ == '__main__':
    main()
