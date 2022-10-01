Changelog
=========

6.0.7 (2022-10-01)
------------------

- Complete es translation
  [erral]

- Complete eu translation
  [erral]
  
- Update po files with new msgids
  [erral]

- Fix some german translations
  [MrTango]

- Fail the release when ``zest.pocompile`` is not available.  [maurits]

- Fix French translations (fuzzy)
  [mpeeters]


6.0.6 (2022-09-02)
------------------

- Change some control panel translations in basque 
  [erral]

- Complete Dutch translations.  
  [jladage]


6.0.5 (2022-08-21)
------------------

- Fixes in Spanish translation: remove fuzzy messages
  [erral]

- Fix Basque translation, remove fuzzy messages
  [erral]

- Fixes in German translation
  [davisagli]


6.0.4 (2022-07-22)
------------------


- Remove transifex configuration. See #325
  [erral]

- Add more Dutch translations, unify the po headers in this language.
  [maurits]

- complete spanish translation
  [erral]

- complete basque translation
  [erral]

6.0.3 (2022-06-26)
------------------

- Update translation files
  [erral]

- Fixes in dutch translations
  [laulaz]

- Fixes in german translations
  [agitator]

- New translations in pat-structure
  [petschki]

- Complete pt-br translation
  [ericof]

6.0.2 (2022-04-06)
------------------

- Fixes Portuguese integrity break message when deleting a content, to consider the
  masculine and feminine gender of the content type.
  [wesleybl]


6.0.1 (2021-12-01)
------------------

- Rename Dexterity Content Types to Content Types in en and de
  [tisto]

- Complete eu translation.
  [erral]


6.0 (2021-10-17)
----------------

- New Serbian situation:

  - Default ``sr`` is now Latin instead of Cyrillic.
  - Copied the Cyrillic translations to ``sr@Cyrl``.
  - Renamed the Latin translations folder from ``sr_Latn`` to ``sr@Latn``.

  If you prefer the Cyrillic character set of this language, set this environment variable:
  ``zope_i18n_allowed_languages sr@Cyrl``
  If you prefer Latin in Plone 5, you can set it to ``sr@Latn`` since Plone 5.2.6 (``plone.i18n 4.0.7``).
  See `issue 326 <https://github.com/collective/plone.app.locales/issues/326>`_.
  [maurits, fredvd]

- Fix French translations.
  [laulaz]


5.1.29 (2021-07-28)
-------------------

- Update Dutch translations.
  [fredvd]

- Fix German translations.
  [pbauer]

- Fix French translations.
  [boulch, laulaz]


5.1.28 (2021-02-20)
-------------------

- Fix French and German translation for the assets folder (no spaces and lowercase).
  [pbauer]

- Fix wrong DE translation in plone.app.caching.
  [jensens]


5.1.27 (2020-11-12)
-------------------

- Use different translations for "User" and "Contributor" in the Italian translation,
  using respectively "Utente" and "Collaboratore".
  [lelit]


5.1.26 (2020-10-12)
-------------------

- Update Italian translations
  [lelit]


5.1.25 (2020-09-22)
-------------------

- Minor fix in German translation.
  [jensens]


5.1.24 (2020-07-14)
-------------------

- For French and Catalan, fix mailtemplate_username_info translation that
  triggered an error when sending the mail.
  This fixes https://github.com/collective/plone.app.locales/issues/311
  [vincentfretin]

- Update Spanish and Basque translations.
  [erral]

- Remove use of html tag in info_empty_dashboard.
  This fixes https://github.com/plone/Products.CMFPlone/issues/3128
  [vincentfretin]

- Update Norwegian translations.
  [espenmn]

- Fix French date and hours format for the pickadate widget.
  [vincentfretin]

- Update german wording and be polite.
  [ksuess]


5.1.23 (2020-06-28)
-------------------

- Update French, German, Spanish, Basque translations.


5.1.22 (2020-06-19)
-------------------

- Update Italian translations
  [ale-rt, arsenico13, cekk, pnicolli]

- Complete Spanish translation for widgets.po
  [erral]

- Basque translations for widgets.po
  [erral]

- Fix typos in French translations.
  [laulaz]

- Fixed possible package install error with Python 3.6 when no system locale is set.
  See `coredev issue 642 <https://github.com/plone/buildout.coredev/issues/642#issuecomment-597008272>`_.
  [maurits]

- German translations for widgets.po.
- Synchronize with latest mockup.
- Structure pattern: Change message from misleading "Cannot order items while querying" to "Drag and drop reordering is disabled while filters are applied.".
  Fixes: https://github.com/collective/plone.app.locales/issues/173
  [thet]


5.1.21 (2020-01-06)
-------------------

- Megaupdate plone.po RU locale.
  [Serge73]


5.1.20 (2019-12-16)
-------------------

- Fix French translation.
  [laulaz]

- Update Japanese translations.


5.1.19 (2019-10-13)
-------------------

- Update Portuguese-BR translations.

- Update French translations.

- Update Slovenian translations, sync from POT files.
  [balavec]

- Update German: Inhalte werden "Erstellt" nicht "Erzeugt".
  [jensens]

- Minor fixes in Basque
  [erral]

- Update Spanish translation.
  [erral]

- Update basque translation
  [erral]

- Update Slovenian translations.
  [balavec]


5.1.18 (2019-07-12)
-------------------

- Update German translations, add most missing.
  [jensens]


5.1.17 (2019-07-03)
-------------------

- Update French, Basque, Catalan translations.


5.1.16 (2019-07-01)
-------------------

- Update French, Basque, Spanish, Norwegian, German translations.


5.1.15 (2019-06-20)
-------------------

- Review French translation.


5.1.14 (2019-06-20)
-------------------

- Add missing french translations.
  [mpeeters]

- Complete Basque translation.
  [erral]

- Updated Chinese Simplified translation.
  [jianaijun]

- Fixed French translations [ale-rt]

5.1.13 (2019-03-05)
-------------------

- Update Italian translations.
  [ale-rt, arsenico13, cekk]
- Add .gitattributes file to avoid most CHANGES merge conflicts
  [@arsenico13]
- Update Traditional Chinese translations.
  [l34marr]
- Update Basque translations.
  [erral]


5.1.12 (2019-01-02)
-------------------

- Fix French translation.
  [laulaz]

- Update Spanish translations.
  [gil-cano]

- Update Traditional Chinese translations.
  [l34marr]


5.1.11 (2018-11-19)
-------------------

- Update Traditional Chinese translations.
  [l34marr]
- Fix small typo in Dutch translation.
  [huubbouma]


5.1.10 (2018-10-02)
-------------------

- Update Traditional Chinese translations.
  [l34marr]
- Save Lithuanian plonelocales with utf-8 encoding. Refs #234
  [pysailor]


5.1.9 (2018-06-08)
------------------

- Update European Portuguese translations.
  [emansije]
- Complete catalan translation.
  [allusa]


5.1.8 (2018-04-01)
------------------

- Complete spanish translation.
  [erral]

- Compelete basque translation.
  [erral]

- Include plone.app.caching translations.
  [erral]

- Include plone.app.multilingual translations.
  [erral]

- Update Brazilian Portuguese translations.
  [hvelarde, agnogueira, lyralemos]

- Update Italian translations.
  [ale-rt, cekk]

- Update German translations.
  [jensens, agitator]

- Update Traditional Chinese translations.
  [l34marr]


5.1.7 (2018-03-11)
------------------

- Got back the 8 messages for the contrain types menu from the 4.3.x branch.
  [vincentfretin]

- Complete widgets translation in spanish.
  [erral]

- Complete Basque translation for widgets.
  [erral]

- Update Traditional Chinese translations.
  [l34marr]

5.1.6 (2018-02-15)
------------------

- Complete Spanish translation.
  [erral]


5.1.5 (2018-02-08)
------------------

- Put back missing translation of password reset mails.
  [allusa, vincentfretin]

- Update Traditional Chinese translations.
  [l34marr]

- Update German translations.
  [jaroel]

5.1.4 (2018-01-24)
------------------

- German fixes and updates
  [staeff]
- Basque fixes
  [erral]
- remove mention of "retina" (https://github.com/plone/Products.CMFPlone/issues/2123)
  [tkimnguyen]
- Basque translation
  [erral]
- Add some German translations for the related items widget
  [cillianderoiste]
- Add German translations for plone.protect dialogs.
  [pgrunewald]
- Update Traditional Chinese translations.
  [l34marr]
- Complete basque (eu) translation
  [erral]

5.1.3 (2017-07-08)
------------------

- Add UK English translation
  [MatthewWilkes]
- Update German translations
  [ksuess]

5.1.2 (2017-04-21)
------------------

- Updated Tranditional Chinese translations.
  [l34marr]

- Fix typo in Italian translation.
  [arsenico13]

5.1.1 (2017-02-21)
------------------

- Update Japanese translations.

- Update the Transifex resourceas configuration at Transifex project
  https://www.transifex.com/plone/plone5/
  [macagua]

- Update Spanish translations.
  [macagua]

- Update basque translations.
  [erral]

- Updated Chinese Simplified translation
  [jianaijun]

- Updated Tranditional Chinese translations.
  [l34marr]


5.1.0 (2016-11-08)
------------------

- Since Products.PasswordResetTool was merged into CMFPlone 5.1 and the templates now use the ``plone`` domain, merge all ``passwordresettool.po`` files into ``plone.po``.
  [thet]


5.0.12 (2016-11-08)
-------------------

- Updated French translations.
  [gnafou]

- Add messages and English translations for portlet manager names.
  [alecm]

- Updated German Translations.
  [vincero]

- Updated Tranditional Chinese translations.
  [l34marr]

- Add coding header to python files.
  [gforcada]

5.0.11 (2016-08-22)
-------------------

- German: Change the querystring criteria group from "Daten" to "Datum".
  It's right, that "Daten" is the plural of "Datum".
  But the naming is misleading and means the same like the english "data".
  [thet]

- German: Change "Ort" to "Path" for translations indicating the hierarchical location of some content.
  Fixes: #117
  [thet]

- Minor German updates.
  [thet]

- Updated Tranditional Chinese translations.
  [l34marr]

- Updated italian translation.
  [keul]


5.0.10 (2016-06-27)
-------------------

- Updated French translation.

- Updated Traditional Chinese translations.
  [l34marr]

- Updated basque translations [erral]

- Updated Dutch translations.  [maurits, fredvd]

- Updated Language-Codes in po file headers.  These headers are not
  used in Plone to determine the language: that is done by inspecting
  the directory name.  But the i18ndude script uses the Language-Code
  header when printing statistics.  Several were set to ``en`` or to
  for example ``zh_CN`` (as the directory name should be) instead of
  ``zh-cn`` (as the language code should be).  [maurits]

- Update German translations.
  [staeff]

- Fix typo in portuguese.
  https://github.com/collective/plone.app.locales/issues/112
  [staeff]

- Update German translations.
  [chrimba]

- Update Traditional Chinese translations.
  [l34marr]

- Fix typos in it translation
  [ale-rt]

- Update Japanese translations for plone.po.
  [terapyon]

- Add russian translate Date and Time Settings, Language Settings and much more in control panel.
  Full Russian translation frontpafe.po
  Translation mocap and widgets
  [serge73]

- add label_schema_default and translate in Japanese
  [terapyon]


5.0.9 (2016-03-02)
------------------

- Update Japanese translations for widgets.po.
  [terapyon]


5.0.8 (2016-03-01)
------------------

- Fix vietnamese error in label_filed_under message.

- Updated it translations
  [ale-rt]

- Updated es translation
  [jpgimenez]

- Updated eu translation
  [erral]

- Updated da_DK translation for registered notify welcome screen.
  [tmog]

- Updated RU translations.
  Correction of translation Tuesday Thursday June July
  [serge73]

- Updated da_DK translations.
  [tmog]

- Fix typo: Fenter -> Fenster
  [agitator]

- Fix typo: shoudl -> should
  [ale-rt]

- Add 7 messages from plone.app.discussion and plone.app.contentmenu.

- Updated pt_BR translations.
  [claytonc]

- Updated pt-BR translations.
  [idgserpro]

- Update Traditional Chinese translations.
  [l34marr]

5.0.7 (2015-12-04)
------------------

- Add 129 messages from plone.app.dexterity and plone.schemaeditor
  with existing translations from those packages.
  [vincentfretin]

- Add 3 new messages from plone.protect
  [vincentfretin]

- Add messages from plone.cachepurging and plone.directives.form packages.
  [vincentfretin]


5.0.6 (2015-11-28)
------------------

- Update Slovenian translations for Plone 5
  [matjazjeran, jcerjak]

- Remove linguaplone translations.
  [vincentfretin]

- Remove locales-future folder that only included russian translations
  for old plone.app.standardtiles, plone.app.deco, plone.app.page versions.
  [vincentfretin]

- Include messages from plone.app.referenceablebehavior and
  plone.app.lockingbehavior
  [vincentfretin]

- Removed all fuzzy markers from dutch translations.
  [jladage]

- Updated pt-BR translations.
  [claytonc, hersonrodrigues]

- Updated Dutch translations
  [coen, dveeze]

- Include plone.protect messages

- Update Traditional Chinese translation.
  [l34marr]

- Update French translation

- Updated Chinese Simplified translation
  [jianaijun]

- Updated Ukrainian translation
  [sorenabell]

- Fixed typos in Italian translations
  [ale-rt]

- Danish translation complete for the first time since 2012. :-)
  [tmog]

- Updated German translations
  [tobiasherp]

5.0.5 (2015-09-28)
------------------

- Some new italian translations
  [ale-rt]

- Update French translation
  [encolpe]


5.0.4 (2015-09-21)
------------------

- Update Basque translation
  [erral]

- Update Italian translation
  [ale-rt]

- Update Traditional Chinese translation.
  [l34marr]

5.0.3 (2015-09-15)
------------------

- Update French translation


5.0.2 (2015-09-07)
------------------

- Update German translation (parts)
  [jensens]

- Update Traditional Chinese translation.
  [l34marr]

5.0.1 (2015-07-24)
------------------

- Update Traditional Chinese translation.
  [l34marr]

- Updated the new link for the renamed 'Types' control panel in all front-pages
  [sneridagh]

- Make configlets titles consistent across the site, first letter capitalized
  [sneridagh]


5.0 (2015-05-15)
----------------

- This release is not compatible with Plone 4.x.
- add widgets.pot file
- Update Traditional Chinese translation.
  [l34marr]
- Update Japanese translation.
  [terapyon]


4.3.5 (2015-04-20)
------------------

- Add 49 messages from plone.app.contenttypes.

- 4 new messages from archetypes.referencebrowserwidget.

- Update Traditional Chinese translation.
  [l34marr]

- Add Dutch translations for new plone.app.portlets and plone.app.collections
  [khink]

- Add en_GB locale

- Add en_AU locale (Australian English translation)

- Fix incorrect usage of spaces in Dutch translation.
  [khink]


4.3.4 (2014-11-01)
------------------

- New messages from plone.app.collection, plone.stringinterp
  and plone.app.portlets (new Actions portlet) for Plone 4.3.4.
  [vincentfretin]

- Update Traditional Chinese translation.
  [l34marr]

- Updated Romanian translation.
  [ichim-david]

- Updated Czech translation.
  [naro]

- Add messages from plone.namedfile and plone.app.textfield packages.
  [vincentfretin]

- New messages from plone.app.querystring (Show inactive filter).
  [vincentfretin]


4.3.3 (2014-02-20)
------------------

- All danish translations are now in UTF-8
  [bosim]

- Updated Romanian translation.
  [ichim-david]

- Update Traditional Chinese translation.
  [marr]

- Added messages for mimetypes.
  French translation.
  [thomasdesvenain]

- Updated Chinese Simplified translation
  [Jian Aijun]

- Updated Spanish translation for plone.app.ldap addon
  [macagua]

- Added Spanish translation for plone.app.caching addon
  [macagua]

- Slovak translation updates
  [rlacko]

- Added Spanish translation for plone.app.ldap addon
  [Talueses]

4.3.2 (2013-08-20)
------------------

- Updated Romanian translation
  [ichim-david]

- Update German translation.
  [jone]

- Updated French translation.

- Updated italian translation
  [keul]


4.3.1 (2013-05-08)
------------------

- Update Dutch translations
  [maartenkling]

- Update Traditional Chinese translations
  [marr]

4.3 (2013-04-10)
----------------

- This version is not compatible with Plone version inferior to 4.3.

- Updated Romanian translation
  [ichimdav]


4.2.5 (2013-01-22)
------------------

- Updated translations.


4.2.4 (2012-12-20)
------------------

- Updated translations.

- Updated Romanian translation for ATContenttypes
  [ichimdav]


4.2.3 (2012-11-26)
------------------

- Updated Finnish translations.


4.2.2 (2012-10-21)
------------------

- Updated translations.

- Added 3 new messages for CMFPlacefulWorkflow, and 2 fuzzies

- Be aware that this release removes 2 translated messages for navigation and
  collection portlets because the English changed. The translation is only
  compatible with Plone 4.2.2.


4.0.15 (2012-08-28)
-------------------

- Updated translations.


4.0.14 (2012-08-19)
-------------------

- Updated translations.


4.0.13 (2012-06-30)
-------------------

- Updated translations.


4.0.12 (2012-05-08)
-------------------

- Updated translations.

- Added messages for new collection type for Plone 4.2


4.0.11 (2012-02-10)
-------------------

- Updated translations.
  [Plone translators]

- 2 new messages in plone.app.ldap domain.

- 4 new messages in plone domain for Plone 4.2b2.


4.0.10 (2011-11-30)
-------------------

- Modified Dutch translations of roles, apply on Plone 4.2 only.
  [khink, vincentfretin]

- Updated translations.
  [Plone translators]


4.0.9 (2011-09-22)
------------------

- Updated translations.
  [Plone translators]

- Added Macedonian (mk_MK) translation.

- Removed zh translations completely, only zh_CN, zh_HK, zh_TW are
  maintained.

- New messages for Plone 4.2.

- New "Sortable Title" message (refs #11238) for Plone 4.2

- Two new messages in cmfplacefulworkflow (Plone 4.0, 4.1, 4.2).

- One new message from plone.app.users 1.1.1 (refs #11842) for Plone 4.1.


4.0.8 (2011-07-13)
------------------

- Updated translations.
  [Plone translators]


4.0.7 (2011-05-15)
------------------

- Two new messages in linguaplone.

- 'Create' message in plone domain appearing in workflow history.

- Updated translations.
  [Plone translators]


4.0.6 (2011-04-05)
------------------

- Updated translations.
  [Plone translators]

- New 'Readers' message for the new reader_emails variable in content rules.
  [vincentfretin]


4.0.5 (2011-02-28)
------------------

- This release includes 10 new messages for Plone 4.1.

- Updated translations.
  [Plone translators]


4.0.4 (2011-01-20)
------------------

- Updated translations.
  [Plone translators]

- Updated indonesian translation
  [dimo]


4.0.3 (2010-11-19)
------------------

- Updated translations.
  [Plone translators]

- Include some Plone 4.1 messages coming from
  plone.app.event and plone.app.collection packages.
  [vincentfretin]


4.0.2 (2010-10-02)
------------------

- Reintroducted translations from the 3.x branch for the
  default_error_message.pt template after the changes revert.
  See http://dev.plone.org/plone/ticket/8667
  [vincentfretin]

- Added some new messages from plone.app.contentrules.
  [Plone translators]


4.0.1 (2010-09-13)
------------------

- Updated translations.
  [Plone translators]

- Addons like plone.app.caching and plone.app.ldap are now in the
  locales-addons folder.
  [vincentfretin]


4.0.0 (2010-08-29)
------------------

- Updated translations.
  [Plone translators]

- Translations of plone.app.caching and plone.app.ldap
  are in this package now.
  [vincentfretin]

- Added titles of default content types views. This closes
  http://dev.plone.org/plone/ticket/10834
  [vincentfretin]


4.0.0rc1 (2010-07-31)
---------------------

- Update license to GPL version 2 only.
  [hannosch]

- Updated translations.
  [Plone translators]


4.0.0b5 (2010-07-03)
--------------------

- Added label and description of relative path criterion. This closes
  http://dev.plone.org/plone/ticket/10711
  [vincentfretin]

- Updated translations.
  [Plone translators]


4.0.0b4 (2010-06-03)
--------------------

- Moved all po and pot files from the i18n folder to the locales folder.
  [vincentfretin]

- Updated translations.
  [Plone translators]


4.0.0b3 (2010-05-01)
--------------------

- Updated translations.
  [Plone translators]


4.0.0b1 (2010-03-06)
--------------------

- Updated translations.
  [Plone translators]


4.0.0a3 (2010-02-01)
--------------------

- Updated translations.
  [Plone translators]


4.0.0a2 (2009-12-02)
--------------------

- Updated translations.
  [Plone translators]


4.0.0a1 (2009-11-18)
--------------------

- Updated translations for Plone 4.
  4.x series are not compatible with Plone 3.x.
  [Plone translators]


3.3.5 (2009-10-31)
------------------

- Added 18 new messages to translate portlet titles and
  descriptions. See http://dev.plone.org/plone/ticket/9631
  [vincentfretin]


3.3.4 (2009-09-05)
------------------

- This release contains .mo files for the locales directory
- Czech: translation update
- French: replaced "Corps du texte" by "Corps de texte"
- German: unfuzzy label_click_here_to_retrieve translation
- Italian: fixed the history_action translation,
  it used ${author} instead of ${actor}


3.3.3 (2009-07-28)
------------------

- Updated translations.
  [Plone translators]


3.3.2 (2009-06-20)
------------------

- Updated translations.
  [Plone translators]


3.3.1 (2009-05-17)
------------------

- Updated translations.
  [Plone translators]


3.3.0 (2009-04-05)
------------------

- Lots of new translations.
  [Plone translators]


3.2.0 (2009-03-02)
------------------

- Added new time_format id to the po files to support the new time_only fix.
  Closes http://dev.plone.org/plone/ticket/8607.
  [jnelson, calvinhp]


3.1.4 (2008-10-13)
------------------

- Restructured the PloneTranslations product into this package.
  The 3.1.4 release contains the same translation files as the
  PloneTranslations 3.1.4 release.
  [hannosch]
