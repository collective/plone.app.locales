======================
Plone Translator's FAQ
======================

About
-----

This document is part of the `Plone Translation Effort`_ documentation. See
`Guidelines for Translators`_ if your question is not covered here. The
`mailing list`_ and IRC_ are two nice ways of getting help.

.. _Plone Translation Effort: http://plone.org/development/i18n
.. _Guidelines for Translators: http://plone.org/development/i18n/translators-guidelines
.. _mailing list: http://plone.org/development/lists
.. _IRC: http://plone.org/development/chat

.. contents::

Access Keys
-----------

*What does ``accesskeys-XY`` as msgid stand for? How do I translate that?*

Accesskeys allow users to access certain parts of the interface through
buttons. Each msgstr must be a single character, e.g. ``s`` for accessing
the search form (see plone-en.po for more examples). A key may not be used
twice.

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
 
Alternatively, you can merge your product-XY.po against product.pot manually and
commit the final version. See `merge.sh`_ in SVN_. It's the shell script that
we use to merge all PO-files with its corresponding product.pot.

.. _merge.sh: http://svn.plone.org/collective/PloneTranslations/trunk/i18n/merge.sh
.. _SVN: http://svn.plone.org/collective/PloneTranslations/trunk/

