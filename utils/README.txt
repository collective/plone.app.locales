Preparing Plone buildout
==========================
::

    git clone -b 5.0 git://github.com/plone/buildout.coredev.git
    cd buildout.coredev
    python2.7 bootstrap.py
    bin/buildout -c experimental/i18n.cfg


Updating translations
=====================

You can find more info on the issue
https://github.com/plone/Products.CMFPlone/issues/983

plone
-----
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

passwordresettool
-----------------
::

    bin/i18n passwordresettool

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
::

    cd locales
    i18ndude sync --pot plonefrontpage.pot */*/plonefrontpage.po

