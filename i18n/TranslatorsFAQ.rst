======================
Plone Translator's FAQ
======================

About
-----

This document is part of the `Plone Translation Effort`_ documentation. See
`Guidelines for Translators`_ if your question is not covered here. The
`mailing list`_ and IRC_ are two nice ways of getting help.

.. _Plone Translation Effort: http://plone.org/development/i18n
.. _Guidelines for Translators: http://plone.org/development/teams/i18n/translators-guidelines
.. _mailing list: http://plone.org/contact/
.. _IRC: http://plone.org/contact/chat

.. contents::

Access Keys
-----------

*Where have all those accesskeys gone?*

Accesskeys are a concept to allow users to access certain parts of the
interface through keyboard shortcuts. Each must be a single character. As these
have caused problems with existing keyboard shortcuts from screen readers
or browsers and operating systems, we have changed these to conform to
internal standards and definied an according set of numerical accesskeys, which
don't need to be changed for different languages.

Fuzzy entries
-------------

*What are "fuzzy" entries?*

From the gettext info pages:

    Fuzzy entries, even if they account for translated entries for most
    other purposes, usually call for revision by the translator.  Those may
    be produced by applying the program 'msgmerge' to update an older
    translated PO files according to a new PO template file, when this tool
    **hypothesises that some new 'msgid' has been modified only slightly out
    of an older one**, and chooses to pair what it thinks to be the old
    translation for the new modified entry.  The slight alteration in the
    original string (the 'msgid' string) should often be reflected in the
    translated string, and this requires the intervention of the
    translator.  For this reason, 'msgmerge' might mark some entries as
    being fuzzy.

In other words, fuzzy entries need revision. The msgstr is intended to help
you with translating the new entry.

Please take your time when reading through the fuzzy marked translations. And
do not forget to remove the fuzzy attribute once you've verified the
translation is ok.

SVN conflicts
-------------

*I have checked out product-XY.po recently from SVN. Now I want to check in
again, but there's already a newer product-XY.po there. The SVN log says it has
been merged with product.pot. What do I do?*
   
Make sure that you are not overwriting someone else's translations. If the only
changes are that the new product-XY.po is merged against product.pot, you can just
commit your work over the old version and drop a note to the mailing list.
