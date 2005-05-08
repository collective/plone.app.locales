#!/bin/bash

PYTHON=/usr/bin/python
I18NDUDE=../../i18ndude/i18ndude

if [ ! -e $I18NDUDE ]; then
    echo "Unable to locate i18ndude utility!"
    exit 1
fi

for PO in plone*.po; do
    if [ $PO != "plone-en.po" ]; then
        $PYTHON $I18NDUDE sync --pot plone.pot -s $PO
    fi
done
