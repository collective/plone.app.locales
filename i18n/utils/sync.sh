#!/bin/bash

PYTHON=/usr/bin/python
I18NDUDE=../../i18ndude/i18ndude

export PYTHON I18NDUDE

$PYTHON sync.py $1
