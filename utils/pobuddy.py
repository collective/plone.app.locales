#!/usr/local/bin/python
# -*-coding: utf-8 -*-

#  poBuddy utility program   $ ./pobuddy -h  for help, tested on OS-X 10.6.
#  Updated by Takeshi Yamamoto (retsu)  tyam AT mac.com   2010/July/19
#      for directory structure change to canonical gettext style
#      for default WYSIWYG editor change from kupu to TinyMCE
#  Created by Takeshi Yamamoto (retsu)  tyam AT mac.com   2009/December/27
#  License: ZPL 2.1 (Zope Public License 2.1)

import sys
import os
import codecs
import operator
import datetime

from optparse import OptionParser

class paraGetter(object):

    def __call__(self):
        para = {}
        para = self.setDefault(para)
        para = self.setArg(para)
        return para

    def setDefault(self, para):

        # set scope of translation files for input
        para['poDir'] = '../i18n'
        para['poLocalesDir'] = '../locales'
        para['poTinyMceDir'] = '../../Products.TinyMCE/Products/TinyMCE/locales'
        para['i18nFiles'] = ['kupu/kupu', 'kupu/kupuconfig', 'kupu/kupupox']
        para['localesFiles'] = ['plone', 'atcontenttypes',
                        'atreferencebrowserwidget', 'passwordresettool',
                        'cmfeditions', 'cmfplacefulworkflow', 'linguaplone',
                        'plonefrontpage', 'plonelocales']
        para['extraFiles'] = ['plone.app.caching', 'plone.app.ldap']
        para['tinyMceFiles'] = ['tinymce', 'plone.tinymce']

        # set scope of languages
        availLangs = os.listdir(para['poLocalesDir'])
        availLangs = [x for x in availLangs \
                     if os.path.isdir(para['poLocalesDir']+'/'+x) == True]
        availLangs = [x for x in availLangs if x != '.svn']
        availLangs = [x for x in availLangs if x != '.DS_Store']
        para['availLangs'] = availLangs
        para['langNames'] = {}

        return para

    def setArg(self, para):

        # parse command line options
        parser = OptionParser()
        usage = "usage: %prog [options] *arg"
        version = "%prog 2.0.0"
        description = "This will generate serveral reports and CSV files from various PO files.  You can specify language codes as arguments.  To get all available feature, '$ ./pobuddy.py -av all' is the easiest way.  Note thiw will create more than 900 CSV files under ./pobuddyCSV directory.  The 'headers.csv' file has valuable information, too.  Example for local translator, eg. Japanese: '$ ./pobuddy.py -swf ja'  For i18n manager: '$ ./pobuddy.py -av all'  For code developers to get POT CSV file to consider consolidating messages: '$ ./pobuddy.py -swf pot'  If you have Products.TinyMCE working copy, 't' option will include po files of TinyMCE."
        parser = OptionParser(usage=usage, version=version, description=description)
        parser.add_option("-s", "--status", action="store_true",
                          dest=("statOn"), default=False,
                          help="show status report")
        parser.add_option("-w", "--warning", action="store_true",
                          dest="warningOn", default=False,
                          help="show warning report")
        parser.add_option("-g", "--graph", action="store_true",
                          dest=("graphOn"), default=False,
                          help="show filled rate graph")
        parser.add_option("-f", "--file", action="store_true",
                          dest=("fileOn"), default=False,
                          help="write CSV files")
        parser.add_option("-p", "--pot", action="store_true",
                          dest=("potOn"), default=False,
                          help="include POT files")
        parser.add_option("-e", "--extra", action="store_true",
                          dest=("extraOn"), default=False,
                          help="include extra (plone.app.*) po files.")
        parser.add_option("-t", "--tiny", action="store_true",
                          dest=("tinyOn"), default=False,
                          help="include tinyMCE files. Products.TinyMCE required")
        parser.add_option("-a", "--all", action="store_true",
                          dest=("allOn"), default=False,
                          help="show all reports and write CSV files")
        parser.add_option("-v", "--verbose", action="store_true",
                          dest="verbose", default=False,
                          help="show progress information")
        parser.add_option("-d", "--directory", action="store",
                          type="string", dest="csvDir", default="./pobuddyCSV",
                          metavar="DIRECTORY",
                          help="specify DIRECTORY for CSV files to be saved." +
                               " Default is ./pobuddyCSV")

        (options, args) = parser.parse_args()

        para['csvDir'] = options.csvDir
        para['warningOn'] = options.warningOn
        para['statOn'] = options.statOn
        para['fileOn'] = options.fileOn
        para['graphOn'] = options.graphOn
        para['potOn'] = options.potOn
        para['verbose'] = options.verbose
        if options.allOn == True:
           para['statOn'] = True
           para['warningOn'] = True
           para['graphOn'] = True
           para['fileOn'] = True
           para['potOn'] = True

        if len(args) == 0:
            para['langs'] = para['availLangs']
            para['potOn'] = True
        else:
            if 'all' in args:
                para['langs'] = para['availLangs']
                para['potOn'] = True
            else:
                para['langs'] = [x for x in args if x in para['availLangs']]
                para['potOn'] = False

        if options.extraOn:
            para['localesFiles'] = para['localesFiles'] + para['extraFiles']

        if options.tinyOn:
            para['files'] = para['localesFiles'] + para['tinyMceFiles'] + para['i18nFiles']
        else:
            para['files'] = para['localesFiles'] + para['i18nFiles']

        para['headerNames'] = ['Project-Id-Version',
                               'POT-Creation-Date',
                               'PO-Revision-Date',
                               'Last-Translator',
                               'Language-Team',
                               'MIME-Version',
                               'Content-Type',
                               'Content-Transfer-Encoding',
                               'Plural-Forms',
                               'Language-Code',
                               'Language-Name',
                               'Preferred-Encodings',
                               'Domain',
                               'X-Is-Fallback-For']

        if para['verbose']:
            print 'AVAILABLE LANG:', para['availLangs']
            print 'LANGUAGE SCOPE:', para['langs']
            print 'FILE SCOPE:', para['files']

        return para

#**************************************************************************

class analyzer(object):

    def __call__(self, para):
        rData = self.analyze(para)
        return rData

    def analyze(self, para):
        # analyze pot and po files
        potTable, potWarningTable, potCsvTable, potHeaderTable = \
                  self.langAnalyzer(para, 'pot', para['files'])
        if para['verbose']:
            print 'POT FILES ANALYZED'
        poCubic = []
        poWarningCubic = []
        poCsvCubic = []
        poHeaderCubic = []
        for lang in para['langs']:
            langStatTable, langWarningTable, langCsvTable, langHeaderTable = \
                       self.langAnalyzer(para, lang, para['files'])
            poCubic.append(langStatTable)
            poWarningCubic.append(langWarningTable)
            poCsvCubic.append(langCsvTable)
            poHeaderCubic.append(langHeaderTable)
            if para['verbose']:
                print 'PO FILES ANALYZED FOR:', lang

        rData = [potTable, potWarningTable, potCsvTable, potHeaderTable, \
                 poCubic, poWarningCubic, poCsvCubic, poHeaderCubic]
        return rData

    def langAnalyzer(self, para, lang, files):
        langStatTable = []
        langWarningTable = []
        langCsvTable = []
        langHeaderTable = []

        for fileName in files:
            para, fileStatLine, fileWarning, fileCsv, fileHeader = \
                          self.fileAnalyzer(para, lang, fileName)
            langStatTable.append(fileStatLine)
            langWarningTable.append(fileWarning)
            langCsvTable.append(fileCsv)
            langHeaderTable.append(fileHeader)
        return langStatTable, langWarningTable, langCsvTable, langHeaderTable

    def fileAnalyzer(self, para, lang, fileName):
        warningLine = []
        fileWarning = []
        fileCsv = []
        fileHeader = {}
        sc = {}
        sc['lang'] = lang
        sc['langName'] = lang
        sc['fileName'] = fileName
        sc['serial'] = 0
        sc['line'] = 0
        sc['msg'] = 0
        sc['filled'] = 0
        sc['vacancy'] = 0
        sc['fuzzy'] = 0
        sc['warning'] = 0
        sc['comment'] = 0
        sc['default'] = 0
        mc = {}
        mc['default'] = u''
        mc['locations'] = u''
        mc['comment'] = u''
        mc['id'] = u''
        mc['idLoc'] = u''
        mc['string'] = u''
        mc['defaultSw'] = False
        mc['idSw'] = False
        mc['stringSw'] = False

        inFile = self.getPath(para, lang, fileName)
        if inFile == False:
            sc['warning'] += 1

            warningMsg = 'FILE NOT FOUND'
            warningRef = fileName
            warningLine = [lang, fileName, 0 , warningMsg, warningRef]
            fileWarning.append(warningLine)

            if para['verbose']:
                print 'INPUT FILE NOT FOUND: ', lang, fileName

            fileStatLine = [lang, sc['langName'], fileName,
                           sc['line'], sc['msg'], sc['filled'], sc['vacancy'],
                           sc['fuzzy'], sc['warning']]
            return para, fileStatLine, fileWarning, fileCsv, fileHeader

        headerOn = True
        fin = codecs.open(inFile, 'r', encoding='utf-8', errors='strict')

        try:
            lines = fin.readlines()
            fin.close()
            fin = codecs.open(inFile, 'r', encoding='utf-8', errors='strict')

        except Exception, em:
            sc['langName'] = 'NOT UTF-8'
            sc['warning'] += 1

            warningMsg = 'FILE NOT ENCODED IN UTF-8'
            warningRef = fileName
            warningLine = [lang, fileName, 0 , warningMsg, warningRef]
            fileWarning.append(warningLine)

            if para['verbose']:
                print 'FILE NOT ENCODED IN UTF-8:', lang, fileName

            fin.close()
            fin = codecs.open(inFile, 'r', encoding='utf-8', errors='replace')

        lines = fin.readlines()
        for line in lines:

            if len(line) == 0:
                sc, fileWarning, fileCsv = \
                    self.makeRec(para, sc, mc, fileWarning, fileCsv)
                break

            sc['line'] += 1

            # PO HEADER INFO COLLECTORS
            if headerOn == True:
                for item in para['headerNames']:
                    if line[:len(item)+2] == '"' + item + ':':
                        fileHeader[item] = line[len(item)+3:-4]

            # PO BODY INFO COLLECTORS

            if line[:2] == '# ':
                wkLine = line[2:]
                #warningLine, fileWarning, sc = \
                #             self.unicodeCheck(para, line, fileWarning, sc)
                if mc['comment'] == '':
                    mc['comment'] = wkLine
                    sc['comment'] += 1
                else:
                    mc['comment'] += ('\n' + wkLine)
                continue

            if line[:11] == '#. Default:':
                wkLine = line[13:-2]
                sc['default'] += 1

                if wkLine == '':
                    mc['defaultSw'] = True
                #else:
                    #warningLine, fileWarning, sc = \
                    #         self.unicodeCheck(para, line, fileWarning, sc)
                mc['default'] = wkLine
                continue

            if line[:4] == '#. "' and mc['defaultSw'] == True:
                wkLine = line[4:-2]
                #warningLine, fileWarning, sc = \
                #             self.unicodeCheck(para, line, fileWarning, sc)
                mc['default'] += wkLine

            if line[:2] == '#:':
                mc['defaultSw'] = False
                if mc['locations'] == u'':
                    mc['locations'] = line[3:-1]
                else:
                    mc['locations'] += ('\n' + line[3:-1])
                continue

            if line[:8] == '#, fuzzy':
                sc['fuzzy'] += 1
                continue

            if line[:5] == 'msgid':
                mc['defaultSw'] = False
                mc['commentSw'] = False
                sc['serial'] += 1
                sc['msg'] += 1
                mc['idLoc'] = str(sc['line'])
                mc['id'] = line[7:-2]

                if mc['id'] == '':
                    mc['idSw'] = True

                #else:
                    #warningLine, fileWarning, sc = \
                    #         self.unicodeCheck(para, line, fileWarning, sc)
                if lang == 'pot' and len(mc['id']) > 100:
                    warningMsg = 'MSGID IS LONGER THAN 100 CHARACTERS'
                    warningRef = 'MSGID: ' + mc['id']
                    warningRef = warningRef + '\n' + 'MSGLOC: ' + mc['locations']
                    warningLine =[lang, fileName, sc['line'],
                                  warningMsg, warningRef]
                    fileWarning.append(warningLine)
                    sc['warning'] += 1

            if line[:6] == 'msgstr':
                mc['idSw'] = False

                mc['string'] = line[8:-2]
                if line[:9] == 'msgstr ""' and mc['id'] == '':
                    sc['serial'] = sc['serial'] - 1
                    sc['msg'] = sc['msg'] -1
                    mc['comment'] = ''
                    mc['default'] = ''
                    mc['locations'] = ''
                    mc['id'] = ''
                    mc['string'] = ''
                    mc['stringSw'] = False

                if line[:9] == 'msgstr ""' and mc['id'] != '':
                    mc['string'] = u''
                    mc['stringSw'] = True

                if line[:9] != 'msgstr ""' and mc['id'] != '':
                    mc['stringSw'] = False
                    wkLine = line[8:-2]
                    # warningLine, fileWarning, sc = \
                    #         self.unicodeCheck(para, line, fileWarning, sc)
                    mc['string'] = wkLine

            if line[:1] == '"':
                wkLine = line[1:-2]
                # warningLine, fileWarning, sc = \
                #             self.unicodeCheck(para, line, fileWarning, sc)
                if mc['stringSw'] == True:
                    mc['string'] += wkLine
                if mc['idSw'] == True:
                    mc['id'] += wkLine

            if len(line) == 1 and mc['id'] != '':
                if mc['string'] == '':
                    sc['vacancy'] += 1
                else:
                    sc['filled'] += 1
                sc, fileWarning, fileCsv = \
                    self.makeRec(para, sc, mc, fileWarning, fileCsv)
                mc = {}
                mc['default'] = u''
                mc['locations'] = u''
                mc['comment'] = u''
                mc['id'] = u''
                mc['idLoc'] = u''
                mc['string'] = u''
                mc['defaultSw'] = False
                mc['idSw'] = False
                mc['stringSw'] = False
                headerOn = False

        fileStatLine = [lang, sc['langName'], fileName,
                       sc['line'], sc['msg'], sc['filled'], sc['vacancy'],
                       sc['fuzzy'], sc['warning']]
        if fileName == 'plone':
            wkLang = fileHeader['Language-Name']
            para['langNames'][lang] = wkLang
            #print
        return para, fileStatLine, fileWarning, fileCsv, fileHeader

    def makeRec(self, para, sc, mc, fileWarning, fileCsv):
        umsgDefault = mc['default']
        umsgString = mc['string']
        mc['idLoc'] = sc['fileName'] + ':' + mc['idLoc']
        csvRec = [str(sc['serial']), sc['lang'], sc['langName'],
                  mc['idLoc'], mc['id'], mc['locations'], umsgDefault,
                  umsgString, mc['comment']]
        fileCsv.append(csvRec)
        if fileWarning == []:
            fileWarning.append([sc['lang'], sc['fileName'], 0, 'NO WARNING', 'NONE'])
        return sc, fileWarning, fileCsv

    def getPath(self, para, lang, fileName):

        inFile = fileName
        if lang in para['langs']:
            if fileName in para['i18nFiles']:
                wkfileName = fileName + '-' + lang + '.po'
                inFile = para['poDir'] + '/' + wkfileName
            else:
                wkfileName = fileName + '.po'
                dashLoc = lang.rfind('-')
                if dashLoc < 0:
                    wklang = lang
                else:
                    wklang = lang[:dashLoc] + '_' + \
                             lang[dashLoc+1:].upper()

                if fileName in para['localesFiles']:
                    inFile = para['poLocalesDir'] + '/' + wklang + \
                             '/LC_MESSAGES/' + wkfileName
                elif fileName in para['tinyMceFiles']:
                    inFile = para['poTinyMceDir'] + '/' + wklang + \
                             '/LC_MESSAGES/' + wkfileName
                else:
                    print '***', wkfile, 'NOT FOUND IN ASSUMED LOCATION'

        elif lang == 'pot':
            wkfileName = fileName + '.pot'
            if fileName in para['i18nFiles']:
                inFile = para['poDir'] + '/' + wkfileName
            if fileName in para['localesFiles']:
                inFile = para['poLocalesDir'] + '/' + wkfileName
            if fileName in para['tinyMceFiles']:
                inFile = para['poTinyMceDir'] + '/' + wkfileName

        if os.path.isfile(inFile) == True:
            pass
        else:
            inFile = False
            pass
        return inFile

#**************************************************************************

class preparator(object):

    def __call__(self, para, rData):
        sData = self.prepStat(para, rData)
        return sData

    def prepStat(self, para, rData):
        poSumTable = []
        potTable, potWarningTable, potCsvTable, potHeaderTable, \
            poCubic, poWarningCubic, poCsvCubic, poHeaderCubic = rData

        # prepare stat data
        potTable.append(self.totalLineMaker(potTable))

        for ix, potLine in enumerate(potTable):
            langNames = para['langNames']
            potLine[1] = para['langNames'][potLine[0]]
            potLine.insert(4, potTable[ix][4])
            filledRate = (100 * potLine[6]) / potLine[4]
            potLine.append(filledRate)

        if len(para['langs']) > 0:
            poCubic, poSumTable = self.reportStat(para, potTable, poCubic)

        if para['verbose']:
            print 'STATISTIC DATA GENERATED'

        potTable, potWarningTable, potCsvTable = \
                  self.potDupInspector(potTable, potWarningTable, potCsvTable)

        if para['verbose']:
            msg = 'POT MSGID DUPLICATION IN DIFFERENT FILES ' + \
                   'WITHIN SAME LANGUAGE INSPECTED'
            print msg

        for ix, lang in enumerate(para['langs']):
            langTable, langWarningTable, langCsvTable = self.langDupInspector(
                       para, poCubic[ix], poWarningCubic[ix], poCsvCubic[ix])

        if para['verbose']:
            msg = 'DIFFERENT PO MSGSTR FOR SAME MSGID IN DIFFERNT ' + \
                   'FILES INSPECTED'
            print msg
        # prepare chart data
        langChart = []
        for poTable in poCubic:
            for poLine in poTable:
                if poLine[2] == u'TOTAL':
                    langChart.append(poLine)
        langChart = sorted(langChart, key=operator.itemgetter(8),reverse=True)
        langChart = sorted(langChart, key=operator.itemgetter(9),reverse=True)
        langChart = sorted(langChart, key=operator.itemgetter(10))
        langChart.reverse()

        if para['verbose']:
            print 'CHART DATA GENERATED'

        sData = [potTable, potWarningTable, potCsvTable, potHeaderTable, \
                 poCubic, poWarningCubic, poCsvCubic, poHeaderCubic, \
                 poSumTable, langChart]
        return sData

    def reportStat(self, para, potTable, poCubic):

        # calcurate total line and add to poCubic
        for poTable in poCubic:
            poTable.append(self.totalLineMaker(poTable))

        # make po summary statistic table
        poSumTable = []
        for ix, irec in enumerate(potTable):
            poSumLine = [u'Total of']
            chosenLang = [poCubic[i][0][0] for i in range(len(poCubic))]
            poSumLine.append(unicode(','.join(chosenLang)))
            poSumLine.append(irec[2])
            poSumLine.append(sum([poCubic[i][ix][3] for i in range(len(poCubic))]))
            poSumLine.append(sum([poCubic[i][ix][4] for i in range(len(poCubic))]))
            poSumLine.append(sum([poCubic[i][ix][5] for i in range(len(poCubic))]))
            poSumLine.append(sum([poCubic[i][ix][6] for i in range(len(poCubic))]))
            poSumLine.append(sum([poCubic[i][ix][7] for i in range(len(poCubic))]))
            poSumLine.append(sum([poCubic[i][ix][8] for i in range(len(poCubic))]))
            poSumTable.append(poSumLine)

        # add POT message count and filled rate values
        for poTable in poCubic:
            for ix, poLine in enumerate(poTable):
                poLine[1] = para['langNames'][poLine[0]]
                poLine.insert(4, potTable[ix][4])
                filledRate = 100 * poLine[6] / poLine[4]
                poLine.append(filledRate)

        for ix, poSumLine in enumerate(poSumTable):
            #poSumLine[1] = para['langNames'][poSumLine[0]]
            poSumLine.insert(4, (potTable[ix][5])*len(poCubic))
            filledRate = 100 * poSumLine[6] / poSumLine[4]
            poSumLine.append(filledRate)

        return poCubic, poSumTable

    def totalLineMaker(self, table):
        sumLine = [table[0][0]]
        sumLine.append(table[0][1])
        sumLine.append(u'TOTAL')
        sumLine.append(sum([table[ix][3] for ix in range(len(table))]))
        sumLine.append(sum([table[ix][4] for ix in range(len(table))]))
        sumLine.append(sum([table[ix][5] for ix in range(len(table))]))
        sumLine.append(sum([table[ix][6] for ix in range(len(table))]))
        sumLine.append(sum([table[ix][7] for ix in range(len(table))]))
        sumLine.append(sum([table[ix][8] for ix in range(len(table))]))
        return sumLine

    def potDupInspector(self, potTable, potWarningTable, potCsvTable):
        # detect duplicateion of msgId in whole pot files.
        wkTable = []
        for ixlang, fileCsvTable in enumerate(potCsvTable):
            for line in fileCsvTable:
                wkTable.append(line)
        wkTable = sorted(wkTable, key=operator.itemgetter(4))
        for ix, item in enumerate(wkTable):
            if ix == 0:
                preItem = item
            else:
                if item[4] == preItem[4]:
                    warningMsg = 'DUPLICATED MSGIDs IN DIFFERENT FILES'
                    warningRef = 'MSGID: ' + preItem[4] + ' MSGIDLOC: ' + \
                                  preItem[3] + ' WITH ' + ' MSGIDLOC: ' + item[3]
                    lang = 'pot'
                    fileName = preItem[3]
                    fileName = fileName[:fileName.rfind(':')]
                    wkMsgLoc = preItem[3]
                    lineCount = int(wkMsgLoc[wkMsgLoc.rfind(':')+1:])
                    warningLine =[lang, fileName, lineCount,
                                  warningMsg, warningRef]
                    potWarningTable.append(warningLine)
                    jx = [potList[2] for potList in potTable].index(fileName)
                    potTable[jx][8] = potTable[jx][8] + 1

                    warningRef = 'MSGID: ' + item[4] + ' MSGIDLOC: ' + \
                                 item[3] + ' WITH ' + ' MSGIDLOC: ' + preItem[3]
                    fileName = item[3]
                    fileName = fileName[:fileName.rfind(':')]
                    wsMsgLoc = item[3]
                    lineCount = int(wkMsgLoc[wkMsgLoc.rfind(':')+1:])
                    warningLine = [lang, fileName, lineCount,
                                   warningMsg, warningRef]
                    potWarningTable.append(warningLine)
                    jx = [poList[2] for poList in potTable].index(fileName)
                    potTable[jx][8] = potTable[jx][8] + 1
                    preItem = item

        return potTable, potWarningTable, potCsvTable

    def langDupInspector(self, para, langTable, langWarningTable, langCsvTable):
        # detect different msgstr for samed msgId in different file
        wkTable = []
        for ixlang, fileCsvTable in enumerate(langCsvTable):
            for line in fileCsvTable:
                wkTable.append(line)
        wkTable = sorted(wkTable, key=operator.itemgetter(4))
        for ix, item in enumerate(wkTable):
            if ix == 0:
                preItem = item
            else:
                if item[4] == preItem[4] and item[7] != preItem[7]:
                    warningMsg = 'DIFFERENT MSGSTR FOR SAME MSGID'
                    warningRef = 'MSGID: ' + item[4] + \
                           ' MSGLOC: ' + preItem[5] + ' MSGSTR: ' + preItem[7] + \
                           ' WITH ' + ' MSGLOC: ' + item[5] + ' MSGSTR: ' + item[7]
                    lang = para['langs'][ix]
                    fileName = preItem[3]
                    fileName = fileName[:fileName.rfind(':')]
                    lineCount = int(preItem[preItem.rfind(':')+1])
                    warningLine =[lang, fileName, lineCount,
                                  warningMsg, warningRef]
                    langWarningTable.append(warningLine)
                    jx = [item[2] for item in langTable].index(fileName)
                    langTable[jx][8] = langTable[jx][8] + 1

                    warningRef = 'MSGID: ' + item[4] + \
                           ' MSGLOC: ' + item[5] + ' MSGSTR: ' + item[7] + \
                           ' WITH ' + ' MSGLOC: ' + preitem[5] + \
                           ' MSGSTR: ' + preitem[7]
                    fileName = item[3]
                    fileName = fileName[:fileName.rfind(':')]
                    lineCount = int(item[item.rfind(':')+1])
                    warningLine =[lang, fileName, lineCount,
                                  warningMsg, warningRef]
                    langWarningTable.append(warningLine)
                    jx = [item[2] for item in langTable].index(fileName)
                    langTable[jx][8] = langTable[jx][8] + 1
                    item = preItem

        return langTable, langWarningTable, langCsvTable


class csvwriter(object):

    def __call__(self, para, rData):
        self.write(para, rData)

    def write(self, para, rData):
        potTable, potWarningTable, potCsvTable, potHeaderTable, \
                 poCubic, poWarningCubic, poCsvCubic, poHeaderCubic = rData

        # print and write results
        if para['fileOn']:
            if os.path.isdir(para['csvDir']):
                msg = 'CSV DIRECTORY EXISTS.  OVERWRITING FILES IN:', \
                       para['csvDir']
                print msg

            self.csvWrite(para, 'pot', potCsvTable)
            for ix, poCsvTable in enumerate(poCsvCubic):
                self.csvWrite(para, para['langs'][ix], poCsvTable)

            # write header CSV file
            outFile = para['csvDir'] + '/' + 'headers.csv'
            fo = codecs.open(outFile, 'w', 'utf-8')
            uline = ['Language', 'File']
            uline.extend(para['headerNames'])
            uline = ['"'+item+'"' for item in uline]
            uline = u','.join(uline) + u'\n'
            fo.write(uline)
            for jx, fileHeader in enumerate(potHeaderTable):
                uline = ['pot', para['files'][jx]]
                for item in para['headerNames']:
                    if item in fileHeader:
                        uline.append(fileHeader[item])
                    else:
                        uline.append('none')
                uline = ['"'+item+'"' for item in uline]
                uline = u','.join(uline) + u'\n'
                fo.write(uline)
            for ix, langHeaderTable in enumerate(poHeaderCubic):
                for jx, fileHeader in enumerate(langHeaderTable):
                    uline = [para['langs'][ix], para['files'][jx]]
                    for item in para['headerNames']:
                        if item in fileHeader:
                            uline.append(fileHeader[item])
                        else:
                            uline.append('none')
                    uline = ['"'+item+'"' for item in uline]
                    uline = u','.join(uline) + u'\n'
                    fo.write(uline)
            fo.close()
            if para['verbose']:
                print 'HEADER CSV FILE WRITTEN:', outFile

    def csvWrite(self, para, lang, csvTable):
        for jx, csvFile in enumerate(csvTable):
            outFile = para['csvDir'] + '/' + para['files'][jx] + \
                      '-' + lang + '.csv'
            fo = codecs.open(outFile, 'w', 'utf-8')
            uline = ['Serial', 'Language', 'Language Name',
                     'MessageID Location', 'MessageID',
                     'Location Message Used', 'Default',
                     'Message String', 'Comment']
            uline = ['"'+item+'"' for item in uline]
            uline = u','.join(uline) + u'\n'
            fo.write(uline)
            for csvLine in csvFile:
                ucsvLine = ['"'+unicode(item)+'"' for item in csvLine]
                uline = u','.join(ucsvLine) + u'\n'
                fo.write(uline)
            fo.close()
        if para['verbose']:
            print 'CSV FILES WRITTEN FOR:', lang

class reporter(object):

    def __call__(self, para, sData):
        self.report(para, sData)

    def report(self, para, sData):
        potTable, potWarningTable, potCsvTable, potHeaderTable, \
                 poCubic, poWarningCubic, poCsvCubic, poHeaderCubic, \
                 poSumTable, langChart = sData

        self.printPotStat(para, potTable)
        if para['potOn'] and para['warningOn']:
            self.printWarning('pot', potWarningTable)

        if len(para['langs']) > 0:
            for ix, lang in enumerate(para['langs']):
                if para['statOn']:
                    self.printStat(poCubic[ix])
                if para['warningOn']:
                    self.printWarning(lang, poWarningCubic[ix])

            if len(para['langs']) > 1:
                self.printStat(poSumTable)
                if para['graphOn']:
                    self.printGraph(langChart, poWarningCubic, para['files'])

    def printPotStat(self,para, table):
        if para['potOn'] and para['statOn']:
            print
            print 'LANGUAGE:', table[0][0], table[0][1]
            title = (
                'FileName                Lines   Items Warning')
            print title
            separator = (
                '--------------------- ------- ------- -------')
            print separator
            for mx in table:
                print '%-21s %7d %7d %7d' \
                % (mx[2][:21],mx[3], mx[5],mx[9])

    def printStat(self, poTable):
        print
        print 'LANGUAGE:', poTable[0][0], poTable[0][1]
        title = (
            'FileName                Lines POTItem   Items  Filled Vacancy '
            'Fuzzy  Warn Fill%')
        print title
        separator = (
            '--------------------- ------- ------- ------- ------- ------- '
            '----- ----- -----')
        print separator
        for mx in poTable:
            print '%-21s %7d %7d %7d %7d %7d %5d %5d %4d%%' \
            % (mx[2][:21],mx[3],mx[4],mx[5],mx[6],mx[7],mx[8],mx[9],mx[10])

    def printWarning(self, lang, table):
        ix = 0
        print
        for line in table:
            for mx in line:
                if mx[3] == 'NO WARNING':
                    pass
                else:
                    ix = ix + 1
                    print ix, mx[0], (mx[1] + ':' + str(mx[2])), \
                          ('*** ' + mx[3] + ' ***'), mx[4]
        if ix == 0:
            # print
            print 'NO WARNING FOUND FOR', lang
        else:
            # print
            print 'TOTAL', ix, 'WARNING FOUND FOR', lang

    def printGraph(self, langChart, poWarningCubic, files):
        print
        print 'FILLED-OUT RATE PER LANGUAGE'
        print
        title = ('Nr LangC Vaca Fuzz Warn Fil% Chart ("*"=2%)')
        print title
        separator = (
            '-- ----- ---- ---- ---- ---- '
            '--------------------------------------------------')
        print separator
        for i, mx in enumerate(langChart):
            bar = '*' * (mx[10] / 2)
            print '%2d %-5s %4d %4d %4d %3d%% %-50s' \
            % (i+1, mx[0][:5], mx[7], mx[8], mx[9], mx[10], bar)

        print
        selected = [item[0] for item in langChart if item[10] >= 80]
        print 'GOLDEN (80-100%):', len(selected), ':', ', '.join(selected)

        print
        selected = [item[0] for item in langChart \
                                  if item[10] >= 50 and item[10] < 80]
        print 'SILVER  (50-79%):', len(selected), ':', ', '.join(selected)

        print
        selected = [item[0] for item in langChart if item[10] < 50]
        print 'BRONZE   (0-49%):', len(selected), ':', ',  '.join(selected)

        print
        print 'FILES NOT ENCODED IN UTF-8:'
        for file in files:
            selectedCount = 0
            selected = []
            for poWarningTable in poWarningCubic:
                for poWarningLine in poWarningTable:
                    for item in poWarningLine:
                        # print 'ITEM: ', item
                        if item[1] == file and item[3] == 'FILE NOT ENCODED IN UTF-8':
                            selected.append(item[0])
                            selectedCount = selectedCount + 1
            selected = sorted(set(selected), key=selected.index)
            if selectedCount > 0:
                print file, ':', len(selected), ':', \
                                      ', '.join(selected)
        print
        print 'PO FILE NOT FOUND:'
        for file in files:
            selectedCount = 0
            selected = []
            for poWarningTable in poWarningCubic:
                for poWarningLine in poWarningTable:
                    for item in poWarningLine:
                        if item[1] == file and item[3] == 'FILE NOT FOUND':
                            selected.append(item[0])
                            selectedCount = selectedCount + 1
            if selectedCount > 0:
                print file, ':', len(selected), ':', \
                                      ', '.join(selected)

def main():

    startTime = datetime.datetime.now()
    print '******************************************** PROCESS BEGINS:', \
               startTime.strftime('%Y-%m-%d %H:%M:%S')

    paraget = paraGetter()
    para = paraget()

    analyze = analyzer()
    rData = analyze(para)

    prepare = preparator()
    sData = prepare(para, rData)

    csvwrite = csvwriter()
    csvwrite(para, rData)

    report = reporter()
    report(para, sData)

    endTime = datetime.datetime.now()
    print
    print '**************************** PROCESS ENDS:', \
           endTime.strftime('%Y-%m-%d %H:%M:%S'), \
          'ELAPSE:', (endTime - startTime).seconds, 'sec.'
    print

if __name__ == '__main__':
    main()

