PloneTranslations
=================

This package contains the translation files for Plone Core and the
LinguaPlone add-on product.

This PloneTranslations version is suitable for both Plone 2.5 and
Plone 3.0.

Information for translators
---------------------------

When translating into your favorite language, you should keep a few
things in mind. First of all, check whether there exists a policy for
your language, for instance with respect to preferred translations of
specific words. This is essential to maintain some consistency. Please
check on:

    http://plone.org/development/teams/i18n/language-specific-terms

Also, read the guidelines for translators on:

    http://plone.org/development/teams/i18n


Then: use tools. There is numerous tools available for making
translations, and keeping your translation files (po files) in sync
with the translation catalog (pot file).

i18ndude is one useful tool for syncing. To sync the pot and po file
for instance, do:

    i18ndude sync --pot <pot filename> <po file> [po file2 ...]


Note that all files in the Subversion repository will always be synced to the
latest pot files, so as long as you check in your changes frequently and do not
keep them on your disk, you shouldn't need to sync anything manually.

For most Linux distro's the 'gettext' package will provide numerous
translation tools. Most important is however the command to check integrity
of your po file:

   msgfmt -c -v <po file>

Make sure to run this command before checking in your files into Subversion.
We also have an automated test suite which will discover syntax errors and a
few of the more typical translation mistakes. Messages which do not pass the
tests will be set to fuzzy. The most common reason is missing or misspelled
message variables (for example: ${name}) in the translated message string.
All variables present in the default text must exist in the translated string
as well.

To make the actual translation, you might use either of PoEdit, KBabel or a
normal text editor. Make sure the editor is able to handle utf-8 encoded text.

Also make sure to check the po headers for consistency. All po editors will
need some configuration as to the project settings, your personal settings,
etc. Check the po file before you start for at least: project name, language
team, language code and language name.

Finally, using a spell-checker when available helps a lot!
