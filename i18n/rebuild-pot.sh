#!/bin/bash

POT=plone.pot-new
LOG=rebuild-pot.log
PYTHON=/usr/bin/python

# Locate Plone dir
PWD=`pwd`
PARENT=`dirname $PWD`

[ -e $PARENT/PloneTool.py ] && PLONE=$PARENT
[ -e $PARENT/CMFPlone/PloneTool.py ] && PLONE=$PARENT/CMFPlone

if [ -z $PLONE ]; then
    echo "Unable to locate Plone dir!"
    exit 1
fi

[ -e $PLONE/../i18ndude/i18ndude ] && I18NDUDE=$PLONE/../i18ndude/i18ndude

if [ -z $I18NDUDE ]; then
    echo "Unable to locate i18ndude utility!"
    exit 2
fi

TEMPLATES=`(find $PLONE/skins -name '*.*pt') | grep -v inplace_calendar`

echo -e "\nRebuilding to $POT - this takes a while, logging to $LOG"
# Using --merge the resulting file is kept sorted by msgid
$PYTHON $I18NDUDE rebuild-pot --pot $POT --create plone --merge manual.pot -s $TEMPLATES >$LOG 2>&1

# Using tail we just append manual.pot to the resulting file
#$PYTHON $I18NDUDE rebuild-pot --pot $POT --create plone -s $TEMPLATES >$LOG 2>&1
#tail -n +22 manual.pot >> $POT

# Remove '## X more:' occurences
sed -ri "/## [0-9]+ more:/d" $POT

# Made paths relative to Plone skins dir
sed -ri "s,$PLONE/skins,\.,g" $POT

# All msgstr's should be empty in the pot
sed -ri "s,msgstr .*,msgstr \"\",g" $POT

echo -e "\nTemplates with unneeded literal msgid:\n"
grep 'Unneeded literal msgid in' $LOG | sed -s 's,Unneeded literal msgid in,,' | sort | uniq
echo -e "\nFull report in rebuild-pot.log\n"

exit 0
