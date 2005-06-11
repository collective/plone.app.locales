#!/usr/bin/env python

"""
   Usage: rescue.py

   As we renamed quite some messages in the last time but translators might
   have based their work on an older copy, this script automates this
   renaming process, so it can safely and repeatedly called on all files,
   looking for 'old-style' messages.

   Note that PYTHON and I18NDUDE must have been set as enviroment variables
   before calling this script
"""

import os, sys
import getopt
from utils import getPoFiles

try:
    from Products.i18ndude import catalog
except ImportError:
    from i18ndude import catalog

__PYTHON = os.environ.get('PYTHON', '')
__I18NDUDE = os.environ.get('I18NDUDE', '')

def main():
    os.chdir('..')

    poFiles = getPoFiles('plone')
    if poFiles == '':
        print 'No po-files were found for the given product.'
        sys.exit(2)

    renamed = {'Exception Log (most recent first)' : 'summary_exception_log',
               'History' : 'summary_history',
               'Returned results' : 'summary_search_results',
               'Review History' : 'summary_review_history',
               'Select roles for each group' : 'summary_roles_for_groups',
               'Events are objects for use in Calendar topical queries on the catalog.' : 'Information about an upcoming event, which can be displayed in the calendar.', # event
               'File objects can contain arbitrary downloadable files.' : 'An external file uploaded to the portal.', # file
               'Image objects can be embedded in pages.' : 'An image, which can be referenced in documents or displayed in an album.', # image
               'Link items are annotated URLs.' : 'A link to an external resource.', # link
               'News Items contain short text articles and carry a title as well as an optional description.' : 'An announcement that will show up on the news portlet and in the news listing.', # news
               'Plone folders can define custom \'view\' actions, or will behave like directory listings without one defined.' : 'A folder which can contain other items.', # folder
               'A placeholder item linking to a \\\"favorite\\\" object in the portal.' : 'A placeholder item linking to a favorite object in the portal.',
               'January' : 'month_jan', 'February' : 'month_feb', 'March' : 'month_mar', 'April' : 'month_apr', 'May' : 'month_may', 'June' : 'month_jun',
               'July' : 'month_jul', 'August' : 'month_aug', 'September' : 'month_sep', 'October' : 'month_oct', 'November' : 'month_nov', 'December' : 'month_dec',
               'Jan' : 'month_jan_abbr', 'Feb' : 'month_feb_abbr', 'Mar' : 'month_mar_abbr', 'Apr' : 'month_apr_abbr', 'Jun' : 'month_jun_abbr',
               'Jul' : 'month_jul_abbr', 'Aug' : 'month_aug_abbr', 'Sep' : 'month_sep_abbr', 'Oct' : 'month_oct_abbr', 'Nov' : 'month_nov_abbr', 'Dec' : 'month_dec_abbr',
               'Monday' : 'weekday_mon', 'Tuesday' : 'weekday_tue', 'Wednesday' : 'weekday_wed', 'Thursday' : 'weekday_thu', 'Friday' : 'weekday_fri',
               'Saturday' : 'weekday_sat', 'Sunday' : 'weekday_sun', 'Mon' : 'weekday_mon_abbr', 'Tue' : 'weekday_tue_abbr', 'Wed' : 'weekday_wed_abbr',
               'Thu' : 'weekday_thu_abbr', 'Fri' : 'weekday_fri_abbr', 'Sat' : 'weekday_sat_abbr', 'Sun' : 'weekday_sun_abbr', 'Mo' : 'weekday_mon_short',
               'Tu' : 'weekday_tue_short', 'We' : 'weekday_wed_short', 'Th' : 'weekday_thu_short', 'Fr' : 'weekday_fri_short', 'Sa' : 'weekday_sat_short',
               'Su' : 'weekday_sun_short', 'Required' : 'title_required'
              }

    for poFile in poFiles:
        try:
            po_ctl = catalog.MessageCatalog(filename=poFile)
        except IOError, e:
            print >> sys.stderr, 'I/O Error: %s' % e

        try:
            msgids = po_ctl.keys()
            for old in renamed.keys():
                if old in msgids:
                    new = renamed.get(old)
                    if new in msgids:
                        print 'New message already in %s' % poFile
                    else:
                        po_ctl[new] = po_ctl.get(old)
                        del po_ctl[old]
                        print 'Rename %s to %s in file %s' % (old, new, poFile)
                else:
                    pass
        except IndexError:
            print poFile

        file = open(poFile+'-new', 'w')
        writer = catalog.POWriter(file, po_ctl)
        writer.write(sort=True)

if __name__ == '__main__':
    main()
