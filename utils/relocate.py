"""
   Usage: relocate.py

   As we moved quite some messages between domains lately, this script
   automates this process, so it can be repeatedly and safely called on po
   files to preserve translations.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys
from utils import getPoFiles, getLanguage

from i18ndude import catalog

__PYTHON = os.environ.get('PYTHON', 'python')
__I18NDUDE = os.environ.get('I18NDUDE', 'i18ndude')

def main():
    os.chdir('..')
    os.chdir('i18n')

    poFilesPlone = getPoFiles('plone')
    if not poFilesPlone:
        print 'No po-files were found for Plone.'
        sys.exit(2)

    poFilesATCT = getPoFiles('atcontenttypes')
    if not poFilesATCT:
        print 'No po-files were found for ATContentTypes.'
        sys.exit(3)

    # format: 'old-domain' : ['msgid1', 'msgid2', ...]
    relocated = {'plone' :
                  ['Changes saved.', 'Please correct the indicated errors.',
                   'Rotate 180', 'help_boolean_criteria_bool',
                   'help_criteria_field_name', 'help_custom_view',
                   'help_custom_view_fields', 'help_date_range_criteria_end',
                   'help_date_range_criteria_start', 'help_exclude_from_nav',
                   'help_limit_number', 'help_news_image', 'help_shortname',
                   'help_path_criteria_value', 'help_string_criteria_value',
                   'help_portal_type_criteria_value', 'help_url',
                   'label_body_text', 'label_boolean_criteria_bool',
                   'label_contact_email', 'label_contact_name',
                   'label_contact_phone', 'label_criteria_field_name',
                   'label_custom_view', 'label_custom_view_fields',
                   'label_date_range_criteria_end', 'label_event_announcement',
                   'label_date_range_criteria_start', 'label_event_attendees',
                   'label_event_end', 'label_event_location',
                   'label_event_start', 'label_event_type',
                   'label_exclude_from_nav', 'label_file', 'label_image',
                   'label_image_caption', 'label_inherit_criteria',
                   'label_item_count', 'label_limit_number', 'label_news_image',
                   'label_path_criteria_recurse', 'label_path_criteria_value',
                   'label_related_items', 'label_short_name',
                   'label_string_criteria_value', 'label_url',
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
                    # We copy over messages for now
                    # del po_ctl[old_domain][relocate_msgid]
                    changes[old_domain] = True

                    new_domain = relocate_domain.get(old_domain)
                    if relocate_msgid in msgids[new_domain]:
                        old_msgstr = po_ctl[new_domain].get(relocate_msgid)
                        if old_msgstr.msgstr == '' and msgstr:
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
                file = open('%s-%s.po' % (domain, lang), 'w')
                writer = catalog.POWriter(file, po_ctl[domain])
                writer.write(sort=True)

if __name__ == '__main__':
    main()
