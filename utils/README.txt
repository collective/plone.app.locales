Preparing Plone 3.3 buildout
============================
The plonenext 3.3 buildout is used to synchronize po files for Plone 3.2 and 3.3::

    mkdir ~/svn
    cd ~/svn
    svn co https://svn.plone.org/svn/plone/plonenext/3.3/ plone3.3
    cd plone3.3

If you plan to synchronize LinguaPlone po files,
you need to add the following line in etc/sources::

    Products.LinguaPlone                  https://svn.plone.org/svn/plone/Products.LinguaPlone/trunk/

The rebuild-pot.py script search a Products directory, let it be happy::

    mkdir Products
    cd src
    svn propset svn:externals -F ../etc/sources  .
    svn up

Products.CMFPlone egg was renamed to Plone, the search algorithm in rebuild-pot.py script needs to be updated.
For now we do a symlink::

    ln -s Plone Products.CMFPlone

::

    cd plone.app.locales/plone/app/locales/utils
    export INSTANCE_HOME=~/svn/plone3.3/


Preparing Plone 4 buildout
==========================
::

    mkdir ~/svn
    cd ~/svn
    svn co https://svn.plone.org/svn/plone/plone-coredev/branches/4.0/ plone4
    cd plone4
    python bootstrap.py
    bin/buildout -c experimental/i18n.cfg
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

    python rebuild-pot.py plone
    python sync.py plone

atcontenttypes
--------------
::

    python rebuild-pot.py atct
    python sync.py atcontenttypes

atreferencebrowserwidget
------------------------
For Plone 3.3, you can use the rebuild-pot.py script (Products.ATReferenceBrowserWidget)::

    python rebuild-pot.py atrbw

For Plone 4, you can't use the rebuild-pot.py script (archetypes.referencebrowserwidget),
use directly the following command::

    i18ndude rebuild-pot --pot atreferencebrowserwidget.pot --create atreferencebrowserwidget --merge atreferencebrowserwidget-manual.pot $INSTANCE_HOME/src/archetypes.referencebrowserwidget

::

   python sync.py atreferencebrowserwidget

passwordresettool
-----------------
::

    python rebuild-pot.py prt
    python sync.py passwordresettool

cmfplacefulworkflow
-------------------
::

    python rebuild-pot.py cmfpw
    python sync.py cmfplacefulworkflow

cmfeditions
-----------
::

    python rebuild-pot.py cmfe
    python sync.py cmfeditions

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

    python rebuild-pot.py lp
    python sync.py linguaplone

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
