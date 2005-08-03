#!/bin/bash

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

export PYTHON PLONE

$PYTHON i18ngenerate.py
