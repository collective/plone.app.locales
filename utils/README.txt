Preparing Plone 3.3 buildout
============================
# This is how I synchronize po files for Plone 3.2 and 3.3 [vincentfretin]

mkdir ~/svn
cd ~/svn
svn co https://svn.plone.org/svn/plone/plonenext/3.3/ plone3.3
cd plone3.3

# If you plan to synchronize LinguaPlone po files,
# you need to add the following line in etc/sources:
# Products.LinguaPlone                  https://svn.plone.org/svn/plone/Products.LinguaPlone/trunk/

# The rebuild-pot.py script search a Products directory, let it be happy
mkdir Products
cd src
svn propset svn:externals -F ../etc/sources  .
svn up
# Products.CMFPlone egg was renamed to Plone, the search algorithm in rebuild-pot.py script needs to be updated.
# For now I do a symlink
ln -s Plone Products.CMFPlone

cd plone.app.locales/plone/app/locales/utils
export INSTANCE_HOME=~/svn/plone3.3/


Preparing Plone 4 buildout
==========================
mkdir ~/svn
cd ~/svn
svn co https://svn.plone.org/svn/plone/plone-coredev/branches/4.0/ plone4
cd plone4
python bootstrap.py
bin/buildout -c i18n.cfg
mkdir Products
cd src
ln -s Plone Products.CMFPlone
cd plone.app.locales/plone/app/locales/utils
export INSTANCE_HOME=~/svn/plone4


Updating translations
=====================
python rebuild-pot.py plone
python sync.py plone

python rebuild-pot.py atct
python sync.py atcontenttypes

python rebuild-pot.py atrbw
python sync.py atreferencebrowserwidget

python rebuild-pot.py prt
python sync.py passwordresettool

python rebuild-pot.py cmfpw
python sync.py cmfplacefulworkflow

python rebuild-pot.py cmfe
python sync.py cmfeditions

python rebuild-pot.py kupu
python sync.py kupu

python rebuild-pot.py kupuconfig
python sync.py kupuconfig

python rebuild-pot.py kupupox
python sync.py kupupox

python rebuild-pot.py lp
python sync.py linguaplone

