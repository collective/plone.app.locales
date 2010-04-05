Preparing Plone 4 buildout
==========================
::

    mkdir ~/svn
    cd ~/svn
    svn co https://svn.plone.org/svn/plone/plone-coredev/branches/4.0/ plone4
    cd plone4
    python bootstrap.py
    bin/buildout -c experimental/i18n.cfg

This is only needed for old rebuild-pot.py script (kupu domains)::

    mkdir Products
    cd src
    ln -s Plone Products.CMFPlone
    cd plone.app.locales/plone/app/locales/utils
    export INSTANCE_HOME=~/svn/plone4


Updating translations
=====================
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

kupu
----
::

    python rebuild-pot.py kupu
    python sync.py kupu

    python rebuild-pot.py kupuconfig
    python sync.py kupuconfig

    python rebuild-pot.py kupupox
    python sync.py kupupox

linguaplone
-----------
::

    bin/i18n linguaplone

plonefrontpage
--------------
::

    cd locales
    i18ndude sync --pot plonefrontpage.pot */*/plonefrontpage.po


SVN externals
=============
::

    plone.app.locales/trunk -> PloneTranslations/trunk
    plone.app.locales/branches/3.x -> PloneTranslations/branches/3.x
    plone.app.locales/branches/3.x/i18n/kupu -> PloneTranslations/trunk/i18n/kupu
    Product.kupu/trunk/i18n -> PloneTranslations/trunk/i18n/kupu
