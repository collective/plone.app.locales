@echo off
rem
rem Usage: find-untranslated.bat <product> <path to products skinsdir>
rem
rem Example: find-untranslated.bat plone d:\zope2\Data\Products\CMFPlone\skins
rem

set PYTHON=D:\zope2\Python\python.exe
set I18NDUDE=D:\zope2\Data\Products\i18ndude\i18ndude
set INSTANCE_HOME=D:\zope2\Data

"%PYTHON%" find-untranslated.py %1 %2