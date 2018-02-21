Preparing Plone buildout
========================

Please read the instructions at
https://docs.plone.org/develop/plone/i18n/contribute_to_translations.html
to have a working install to work on translations.


Updating translations
=====================

You can find more info on the issue
https://github.com/plone/Products.CMFPlone/issues/983

plone
-----
From the plone buildout:

::

    bin/i18n plone

atcontenttypes
--------------
::

    bin/i18n atcontenttypes

atreferencebrowserwidget
------------------------
::

    bin/i18n atreferencebrowserwidget

cmfplacefulworkflow
-------------------
::

    bin/i18n cmfplacefulworkflow

cmfeditions
-----------
::

    bin/i18n cmfeditions

linguaplone
-----------
::

    bin/i18n linguaplone

plonefrontpage
--------------

The plonefrontpage.pot is maintained manually.
To resync the po files:

::

    cd locales
    i18ndude sync --pot plonefrontpage.pot */*/plonefrontpage.po

