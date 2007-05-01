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

    products = ['plone','atreferencebrowserwidget','atcontenttypes','archetypes']
    poFiles = {}

    for product in products:
        poFiles[product] = getPoFiles(product)
        if not poFiles[product]:
            print 'No po-files were found for %s.' % product
            sys.exit(2)

    renamed = {}
    renamed['plone'] = {
            'Exception Log (most recent first)' : 'summary_exception_log', 'History' : 'summary_history',
            'Returned results' : 'summary_search_results', 'Review History' : 'summary_review_history',
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
            'Su' : 'weekday_sun_short', 'Required' : 'title_required', 'Add' : 'label_add', 'Add Comment' : 'label_add_comment', 'Add New Group' : 'label_add_new_group', 
            'Add New User' : 'label_add_new_user', 'Add user to selected groups' : 'label_add_user_to_group', 
            'Add selected users to this group' : 'label_add_users_to_group', 'Usable in any browser' : 'label_any_browser', 
            'Apply Changes' : 'label_apply_changes', 'Apply Settings' : 'label_apply_settings', 'Assign Local Role to Selected User(s)' : 'label_assign_local_role_to_users', 
            'Assign Local Role to Selected Group(s)' : 'label_assign_role_to_groups', 'Assign Selected Role(s) to Selected User(s)/Group(s)' : 'label_assign_roles_to_users_groups', 
            'Cancel' : 'label_cancel', 'Change Comment' : 'label_change_comment', 'Change contributers' : 'label_change_contributers', 
            'Change ownership' : 'label_change_ownership', 'Change Password' : 'label_change_password', 
            'Clear Displayed Entries' : 'label_clear_displayed_entries', 'Compare' : 'label_compare', 'Copy to present' : 'label_copy_to_present', 
            'Valid CSS' : 'label_css', 'Delete Selected Role(s) and User(s)/Group(s)' : 'label_delete_roles_users_groups', 
            'Disable Syndication' : 'label_disable_syndication', 'This document is locked.' : 'label_document_locked', 
            'Enable syndication' : 'label_enable_syndication', 'Install' : 'label_install', 'Log in' : 'label_log_in', 
            'Log in to add comments' : 'label_login_to_add_comments', 'Log in to send feedback' : 'label_login_to_send_feedback', 
            'Object locked' : 'label_object_locked', 'Ok' : 'label_ok', 'Perform Search' : 'label_perform_search', 
            'Powered by Plone' : 'label_powered_by_plone', 'Refresh' : 'label_refresh', 'Register' : 'label_register', 
            'Remove' : 'label_remove', 'Remove selected groups' : 'label_remove_selected_groups', 'Remove selected users' : 'label_remove_selected_users', 
            'Rename All' : 'label_rename_all', 'Reply' : 'label_reply', 'RSS Feed' : 'label_rss_feed', 'Save' : 'label_save', 
            'Search' : 'label_search', 'Section 508' : 'label_section_508', 'Select all items' : 'label_select_all_items', 
            'Send' : 'label_send', 'Send me my password' : 'label_send_my_password', 'Show all entries' : 'label_show_all_entries', 
            'Undo' : 'label_undo', 'Uninstall' : 'label_uninstall', 'Use Selected...' : 'label_use_selected', 
            'Username' : 'label_username', 'WCAG' : 'label_wcag', 'Valid XHTML' : 'label_xhtml', 'Add comment' : 'legend_add_comment', 
            'Calendar' : 'summary_calendar', 'Add new items in the same folder as this item' : 'title_add_new_items_inside_folder', 
            'Add new items inside this item' : 'title_add_new_items_inside_item', 'This Plone site is usable in any web browser.' : 'title_any_browser', 
            'This Plone site was built using the Plone Content Management System. Click for more information.' : 'title_built_with_plone', 
            'Change default page' : 'title_change_default_page', 'Change the item used as default view in this folder' : 'title_change_default_view_item', 
            'Change the state of this item' : 'title_change_state_of_item', 'Choose default view' : 'title_choose_default_view', 
            'Configure which content types can be added here' : 'title_configure_addable_content_types', 'This Plone site was built with valid CSS.' : 'title_css', 
            'This Plone site was built with valid CSS and semantically correct use of tables.' : 'title_css_with_semantically_correct_tables', 
            'Move item down' : 'title_move_item_down', 'Move item up' : 'title_move_item_up', 'Relevance' : 'title_relevance', 
            'Delete or rename the index_html item to gain full control over how this folder is displayed.' : 'title_remove_index_html_for_display_control', 
            'RSS feed of these search results' : 'title_rss_feed', 'Search Site' : 'title_search_site', 
            'This Plone site conforms to the US Government Section 508 Accessibility Guidelines.' : 'title_section_508', 
            'Select default page' : 'title_select_default_page', 'Select an item to be used as default view in this folder' : 'title_select_default_view_item', 
            'Send a mail to this user' : 'title_send_mail_to_user', 'Show all available content types' : 'title_show_all_content_types', 
            'This Plone site conforms to the W3C-WAI Web Content Accessibility Guidelines.' : 'title_wcag', 
            'This Plone site is valid XHTML.' : 'title_xhtml', 'legend_comment_details' : 'legend_add_comment', 
            'box_sign_in' : 'Log in', 'listingheader_undo' : 'Undo', 'help_user_name_caps' : 'help_login_name_caps',
            'description_signin_fail_cookies_link' : 'description_login_fail_enable_cookies',
            'Add ${type} to folder' : 'label_add_type_to_folder', 'accessibility' : 'Accessibility',
            'RSS feed of this folder\'s contents' : 'RSS feed of this listing', 'Standard listing' : 'Standard view',
            'Tile view' : 'Summary view'
           }

    renamed['atreferencebrowserwidget'] = {
            'No reference set. Click the browse button to select.' : 'label_no_reference_set', 'Browse...' : 'label_browse',
            'Remove reference' : 'label_remove_reference', 'Remove selected items' : 'label_remove_selected_items'
           }

    renamed['atcontenttypes'] = {
            'Execute' : 'label_execute', 'text_no_albuns_uploaded' : 'text_no_albums_uploaded',
            'constraintypes_disabled_label' : 'constraintypes_disable_label', 'constraintypes_enabled_label' : 'constraintypes_enable_label'
           }

    renamed['archetypes'] = {
            'Previous' : 'label_previous', 'Next' : 'label_next'
           }

    for product in products:
        for poFile in poFiles[product]:
            try:
                po_ctl = catalog.MessageCatalog(filename=poFile)
            except IOError, e:
                print >> sys.stderr, 'I/O Error: %s' % e

            changed = False
            msgids = po_ctl.keys()
            for old in renamed[product].keys():
                if old in msgids:
                    new = renamed[product].get(old)
                    if not new in msgids:
                        po_ctl[new] = po_ctl.get(old)
                        del po_ctl[old]
                        changed = True
                        print 'Rename %s to %s in file %s' % (old, new, poFile)

            if changed:
                file = open(poFile+'-new', 'w')
                writer = catalog.POWriter(file, po_ctl)
                writer.write(sort=True)

if __name__ == '__main__':
    main()
