@echo off
rem
rem Usage: rebuild-pot.bat <product> <path to products skinsdir>
rem
rem Example: rebuild-pot.bat plone d:\zope2\Data\Products\CMFPlone\skins
rem

set PYTHON=D:\zope2\Python\python.exe
set I18NDUDE=D:\zope2\Data\Products\i18ndude\i18ndude
set INSTANCE_HOME=D:\zope2\Data

"%PYTHON%" rebuild-pot.py %1 %2
