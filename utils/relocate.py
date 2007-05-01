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

    poFilesAT = getPoFiles('archetypes')
    if not poFilesAT:
        print 'No po-files were found for Archetypes.'
        sys.exit(3)

    # format: 'old-domain' : ['msgid1', 'msgid2', ...]
    # currently only relocating between archetypes and plone and vica versa is possibly
    relocated = {'plone' :
                  ['description_edit_properties', 'heading_edit_item',
                   'label_existing_keywords', 'label_new_keywords'
                  ]
                }

    # make sure we only try on languages for which both po files exist
    ploneLanguages = [getLanguage('plone', p) for p in poFilesPlone]
    atLanguages = [getLanguage('archetypes', p) for p in poFilesAT]

    languages = [l for l in ploneLanguages if l in atLanguages and l != 'en']
    changes = {'plone' : False, 'archetypes' : False}

    for lang in languages:
        po_ctl = {}
        try:
            po_ctl['plone'] = catalog.MessageCatalog(filename='plone-%s.po' % lang)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e
        try:
            po_ctl['archetypes'] = catalog.MessageCatalog(filename='archetypes-%s.po' % lang)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e

        changes = {'plone' : False, 'archetypes' : False}

        relocate_domain = {'plone' : 'archetypes', 'archetypes' : 'plone'}

        msgids = {}
        msgids['plone'] = po_ctl['plone'].keys()
        msgids['archetypes'] = po_ctl['archetypes'].keys()

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
