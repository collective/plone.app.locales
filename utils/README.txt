# This is how I synchronize po files [vincentfretin]
#
# Plone 3.3 adds 4 new translatable strings compared to Plone 3.2. And remove 3 strings if you count r25302 (https://dev.plone.org/plone/changeset/25302).

mkdir -p ~/svn
cd ~/svn
svn co http://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/3.2/ buildout-plone-3.2
cd buildout-plone-3.2
mkdir Products
cd src
svn export http://svn.plone.org/svn/plone/plonenext/3.3/etc/sources EXTERNALS.txt
svn propset svn:externals -F EXTERNALS.txt  .
svn up
ln -s Plone Products.CMFPlone

cd Plone/Products/CMFPlone
svn merge -r25302:25301 .
cd -

cd plone.app.locales/plone/app/locales/utils
export INSTANCE_HOME=~/svn/buildout-plone-3.2/

python rebuild-pot.py plone
python sync.py plone

python rebuild-pot.py atct
python sync.py atcontenttypes

python rebuild-pot.py atrbw
python sync.py atreferencebrowserwidget

#python rebuild-pot.py plt
#python sync.py plonelanguagetool

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

