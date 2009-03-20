# This is how I synchronize po files for Plone 3.2 and 3.3 [vincentfretin]

mkdir -p ~/svn
cd ~/svn
svn co https://svn.plone.org/svn/plone/plonenext/3.3/ plonenext3.3i18n
cd plonenext3.3i18n
# The rebuild-pot.py script search a Products directory, let it be happy
mkdir Products
cd src
svn propset svn:externals -F ../etc/sources  .
svn up
# Products.CMFPlone egg was renamed to Plone, the search algorithm in rebuild-pot.py script needs to be updated.
# For now I do a symlink
ln -s Plone Products.CMFPlone

# to keep 3 strings for Plone 3.2 (https://dev.plone.org/plone/changeset/25302)
cd Plone/Products/CMFPlone
svn merge -r25302:25301 .
cd -

# to keep the History string for Plone 3.2
cd Products.CMFEditions/Products/CMFEditions/profiles/default
svn export https://svn.plone.org/svn/collective/Products.CMFEditions/branches/1.1/Products/CMFEditions/profiles/default/actions.xml

cd plone.app.locales/plone/app/locales/utils
export INSTANCE_HOME=~/svn/plonenext3.3i18n/

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

