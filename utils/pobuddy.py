#!/usr/bin/python

#  poBuddy utility program   $ ./pobuddy -h  for help, tested on OS-X 10.6.
#  Created by Takeshi Yamamoto (retsu)  tyam AT mac.com   2009/December/27
#  License: ZPL 2.1 (Zope Public License 2.1)

import sys
import os
import codecs
import glob
import operator
import datetime

from optparse import OptionParser

def main():
    global poDir, poLocalesDir, i18nFiles, localesFiles, headerNames, verbose

    # parse command line options
    parser = OptionParser()
    usage = "usage: %prog [options] *arg"
    version = "%prog 1.0.3"
    description = "This will generate serveral reports and CSV files from various PO files.  You can specify language codes as arguments.  To get all available feature, '$ ./pobuddy.py -av all' is the easiest way.  Note thiw will create more than 900 CSV files under ./pobuddyCSV directory.  The 'headers.csv' file has valuable information, too.  Example for local translator, eg. Japanese: '$ ./pobuddy.py -swf ja'  For i18n manager: '$ ./pobuddy.py -av all'  For code developers to get POT CSV file to consider consolidating messages: '$ ./pobuddy.py -swf pot'"
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

    # set parameters
    poDir = '../i18n'
    poLocalesDir = '../locales'
    csvDir = options.csvDir
    warningOn = options.warningOn
    statOn = options.statOn
    fileOn = options.fileOn
    graphOn = options.graphOn
    verbose = options.verbose
    if options.allOn == True:
       statOn = True
       warningOn = True
       graphOn = True
       fileOn = True

    if verbose:
        startTime = datetime.datetime.now()
        print '******************************************** PROCESS BEGINS:', \
               startTime.strftime('%Y-%m-%d %H:%M:%S')
    # set scope of languages
    wkNames = glob.glob(poDir+'/plone-*.po')
    availLangs = [iName[7+iName.rfind('/'):-3] for iName in wkNames]
    langs = []
    if len(args) == 0:
        args = ['en']    # set default for no argument
    if 'all' in args:
        langs = availLangs
    else:
        for item in args:
            if item in availLangs:
                langs.append(item) 
            elif item == 'pot' or item == 'en':
                pass
            else:
                print 'Wrong language code specified:', args
                print 'Available languages:', ', '.join(availLangs)
                return

    # set scope of translation files for input
    i18nFiles = ['plone', 'atcontenttypes', 
                 'atreferencebrowserwidget', 'passwordresettool',
                 'cmfeditions', 'cmfplacefulworkflow', 'linguaplone', 
                 'kupu/kupu', 'kupu/kupuconfig', 'kupu/kupupox']
    localesFiles = ['plonefrontpage', 'plonelocales']

    files = i18nFiles
    files.extend(localesFiles)

    if verbose:
        print 'LANGUAGE SCOPE:', ', '.join([item for item in langs])
        print 'FILE SCOPE:', ', '.join([item for item in files])

    # analyze pot and po files
    potTable, potWarningTable, potCsvTable, potHeaderTable = \
                                            langAnalyzer('pot', files)
    if verbose:
        print 'POT FILES ANALYZED'
    poCubic = []
    poWarningCubic = []
    poCsvCubic = []
    poHeaderCubic = []
    for lang in langs:
        langTable, langWarningTable, langCsvTable, langHeaderTable = \
                                                   langAnalyzer(lang, files)
        poCubic.append(langTable)
        poWarningCubic.append(langWarningTable)
        poCsvCubic.append(langCsvTable)
        poHeaderCubic.append(langHeaderTable)
        if verbose:
            print 'PO FILES ANALYZED FOR:', lang

    # prepare stat data
    potTable.append(totalLineMaker(potTable))

    for ix, poLine in enumerate(potTable):
        poLine.insert(4, potTable[ix][4])
        filledRate = (100 * poLine[6]) / poLine[4]
        poLine.append(filledRate)

    if len(langs) > 0:
        poCubic, poSumTable = reportStat(potTable, poCubic)

    if verbose:
        print 'STATISTIC DATA GENERATED'

    potTable, potWarningTable, potCsvTable = \
              potDupInspector(potTable, potWarningTable, potCsvTable)

    if verbose:
        msg =  'POT MSGID DUPLICATION IN DIFFERENT FILES ' + \
               'WITHIN SAME LANGUAGE INSPECTED'
        print msg

    for ix, lang in enumerate(langs):
        langTable, langWarningTable, langCsvTable = langDupInspector(
                   langs, poCubic[ix], poWarningCubic[ix], poCsvCubic[ix])

    if verbose:
        print 'DIFFERENT PO MSGSTR FOR SAME MSGID IN DIFFERNT FILES INSPECTED'

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

    if verbose:
        print 'CHART DATA GENERATED'

    # print and write results
    if fileOn:
        for file in files:
            outFile = csvDir + '/' + file + '-pot.csv' 
            if outFile.count('/') > 1:
                try:
                    os.makedirs(outFile[:outFile.rfind('/')])
                except OSError as error:
                    if error[0] == 17:
                        if verbose:
                            print 'CSV DIRECTORY ALREADY EXISTS:', error
        csvWriter('pot', files, potCsvTable, csvDir)
        for ix, poCsvTable in enumerate(poCsvCubic):
            csvWriter(langs[ix], files, poCsvTable, csvDir)

        # write header CSV file
        outFile = csvDir + '/' + 'headers.csv'
        fo = codecs.open(outFile, 'w', 'utf-8')
        uline = ['Language', 'File']
        uline.extend(headerNames)
        uline = ['"'+item+'"' for item in uline]
        uline = u','.join(uline) + u'\n' 
        fo.write(uline)
        for jx, fileHeader in enumerate(potHeaderTable):
            uline = ['pot', files[jx]]
            for item in headerNames:
                if item in fileHeader:
                    uline.append(fileHeader[item])
                else:
                    uline.append('none')
            uline = ['"'+item+'"' for item in uline]
            uline = u','.join(uline) + u'\n'
            fo.write(uline)
        for ix, langHeaderTable in enumerate(poHeaderCubic):
            for jx, fileHeader in enumerate(langHeaderTable):
                uline = [langs[ix], files[jx]]
                for item in headerNames:
                    if item in fileHeader:
                        uline.append(fileHeader[item])
                    else:
                        uline.append('none')
                uline = ['"'+item+'"' for item in uline]
                uline = u','.join(uline) + u'\n'
                fo.write(uline)
        fo.close()
        if verbose:
            print 'HEADER CSV FILE WRITTEN:', outFile

    if len(langs) == 0 or 'all' in args  or 'pot' in args or 'en' in args:
        if statOn:
            printPotStat(potTable)
        if warningOn:
            printWarning('pot', potWarningTable)

    if len(langs) > 0:
        for ix, lang in enumerate(langs):
            if statOn:
                printStat(poCubic[ix])
            if warningOn:
                printWarning(lang, poWarningCubic[ix])

        if len(langs) > 1:
            printStat(poSumTable)
            if graphOn:
                printGraph(langChart, poWarningCubic, files)
    print 
    if verbose:
        endTime = datetime.datetime.now()
        print '**************************** PROCESS ENDS:', \
               endTime.strftime('%Y-%m-%d %H:%M:%S'), \
              'ELAPSE:', (endTime - startTime).seconds, 'sec.'
    print

def potDupInspector(potTable, potWarningTable, potCsvTable):
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

def langDupInspector(langs, langTable, langWarningTable, langCsvTable):
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
                lang = langs[ix]
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

def csvWriter(lang, files, csvTable, csvDir):
    for jx, csvFile in enumerate(csvTable):
        outFile = csvDir + '/' + files[jx] + '-' + lang + '.csv' 
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
    if verbose:
        print 'CSV FILES WRITTEN FOR:', lang

def printGraph(langChart, poWarningCubic, files):
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
    print
    print 'UNICODE DECODE ERROR:'
    for file in files:
        selectedCount = 0
        selected = []
        for poWarningTable in poWarningCubic:
            for poWarningLine in poWarningTable:
                for item in poWarningLine:
                    if item[1] == file and item[3] == 'UNICODE DECODE ERROR':
                        selected.append(item[0])
                        selectedCount = selectedCount + 1
        selected = sorted(set(selected), key=selected.index)
        if selectedCount > 0:
            print file, ':', len(selected), ':', \
                                  ', '.join(selected)

def printWarning(lang, table):
    ix = 0
    for line in table:
        for mx in line:
            if mx[3] == 'NO WARNING FOUND':
                pass
            else:
                ix = ix + 1
                print
                print ix, mx[0], (mx[1] + ':' + str(mx[2])), \
                      ('*** ' + mx[3] + ' ***'), mx[4]
    if ix == 0:
        print
        print 'NO WARNING FOUND FOR', lang
    else:
        print
        print 'TOTAL', ix, 'WARNING FOUND FOR', lang

def reportStat(potTable, poCubic):    

    # calcurate total line and add to poCubic    
    for poTable in poCubic:
        poTable.append(totalLineMaker(poTable))

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
            poLine.insert(4, potTable[ix][4])
            filledRate = 100 * poLine[6] / poLine[4]
            poLine.append(filledRate)

    for ix, poSumLine in enumerate(poSumTable):
        poSumLine.insert(4, (potTable[ix][5])*len(poCubic))
        filledRate = 100 * poSumLine[6] / poSumLine[4]
        poSumLine.append(filledRate)

    return poCubic, poSumTable

def totalLineMaker(table):
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

def printPotStat(table):
    print
    print 'LANGUAGE:', table[0][0], table[0][1]
    title = (
        'FileName          Lines   Items Warning')
    print title
    separator = (
        '--------------- ------- ------- -------')
    print separator
    for mx in table:
        print '%-15s %7d %7d %7d' \
        % (mx[2][:15],mx[3], mx[5],mx[9])

def printStat(poTable):
    print
    print 'LANGUAGE:', poTable[0][0], poTable[0][1]
    title = (
        'FileName          Lines POTItem   Items  Filled Vacancy '
        '  Fuzzy Warning Filled%')
    print title
    separator = (
        '--------------- ------- ------- ------- ------- ------- '
        '------- ------- -------')
    print separator
    for mx in poTable:
        print '%-15s %7d %7d %7d %7d %7d %7d %7d %6d%%' \
        % (mx[2][:15],mx[3],mx[4],mx[5],mx[6],mx[7],mx[8],mx[9],mx[10])

def langAnalyzer(lang, files):
    global verbose
    langStatTable = []
    langWarningTable = []
    langCsvTable = []
    langHeaderTable = []

    for fileName in files:
        fileStatLine, fileWarning, fileCsv, fileHeader = \
                                            fileAnalyzer(lang, fileName)
        langStatTable.append(fileStatLine)
        langWarningTable.append(fileWarning)
        langCsvTable.append(fileCsv)
        langHeaderTable.append(fileHeader)
    return langStatTable, langWarningTable, langCsvTable, langHeaderTable

def fileAnalyzer(lang, fileName):
    global poDir, poLocalesDir, i18nFiles, localesFiles, headerNames, veorbose
    warningLine = []
    fileWarning = [[]]
    fileCSV = []
    fileHeader = {}
    serialCount = 0
    warningCount = 0
    lineCount = 0
    msgCount = 0
    filledCount = 0
    vacancyCount = 0
    fuzzyCount = 0
    commentCount = 0
    defaultCount = 0
    langName = ''
    ulangName = u''
    msgDefault = ''
    msgLocations = ''
    msgComment = ''
    msgId = ''
    msgString = ''
    msgStringSw = False
    msgIdSw = False
    msgDefaultSw = False
    headerNames = ['Project-Id-Version',
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

    if lang == 'pot':
        wkfileName = fileName + '.pot'
        if fileName in i18nFiles:
            inFile = poDir + '/' + wkfileName
        if fileName in localesFiles:
            inFile = poLocalesDir + '/' + wkfileName
    else:
        if fileName in i18nFiles:
            wkfileName = fileName + '-' + lang + '.po'
            inFile = poDir + '/' + wkfileName
        if fileName in localesFiles:
            wkfileName = fileName + '.po'
            dashLoc = lang.rfind('-')
            if dashLoc < 0:
                wklang = lang
            else:
                wklang = lang[:dashLoc] + '_' + \
                         lang[dashLoc+1:].upper()
            inFile = poLocalesDir + '/' + wklang + '/LC_MESSAGES/' + wkfileName

    try: 
        f = open(inFile, 'r')

    except IOError as error:
        fileStatLine = [lang, 'FILE NOT FOUND:', fileName, 0, 0, 0, 0, 0, 1]
        warningMsg = 'FILE NOT FOUND'
        warningRef = inFile
        warningLine = [lang, fileName, 0 , warningMsg, warningRef]
        if fileWarning == [[]]:
            fileWarning = [warningLine]
        else:
            fileWarning.append(warningLine)
        warningCount = warningCount + 1
        if verbose:
            print 'INPUT FILE NOT FOUND:', lang, fileName
        return fileStatLine, fileWarning, fileCSV, fileHeader

    lines = f.readlines()
    f.close()

    for line in lines:
        lineCount = lineCount + 1

        # PO HEADER INFO COLLECTORS
     
        for item in headerNames:
            if line[:len(item)+2] == '"' + item + ':':
                itemKey = item
                itemValue = line[len(item)+3:-4]
                try:
                    itemValue = itemValue.decode('utf-8')
                    if itemKey == 'Language-Name':
                        langName = unicode(itemValue)
                        ulangName = langName
                except Exception, em:
                    if itemKey == 'Language-Name':
                        langName = 'LangName utf-8 Error"'
                        ulangName = langName
                    warningMsg = 'UNICODE DECODE ERROR'
                    warningRef = 'PO HEADER: ' + line[:-1] + \
                                 ', EXCEPTION: \'' + em.args[0] + '\'' + \
                                 ' codec can\'t decode byte ' + em.args[1] + \
                                 ' in position ' + \
                                  str(em.args[2]) + '-' + str(em.args[3]) + \
                                 ': ' + em.args[4]
                    warningLine = [lang, fileName, lineCount, warningMsg,
                                   warningRef]
                    if fileWarning == [[]]:
                        fileWarning = [warningLine]
                    else:
                        fileWarning.append(warningLine)
                    warningCount = warningCount + 1
                fileHeader[itemKey] = itemValue

        # PO BODY INFO COLLECTORS

        if line[:2] == '# ':
            wkLine = line[2:]
            try:
                wkLine = wkLine.decode('utf-8')
            except Exception, em:
                warningMsg = 'UNICODE DECODE ERROR'
                warningRef = line[:-1] + \
                             ', EXCEPTION: \'' + em.args[0] + '\'' + \
                             ' codec can\'t decode byte ' + em.args[1] + \
                             ' in position ' + \
                              str(em.args[2]) + '-' + str(em.args[3]) + \
                             ': ' + em.args[4]
                warningLine =[lang, fileName, lineCount, \
                              warningMsg, warningRef]
                if fileWarning == [[]]:
                    fileWarning = [warningLine]
                else:
                    fileWarning.append(warningLine)
                warningCount = warningCount + 1
                wkLine = u'***UTF-8 DECODE ERROR***'
            if msgComment == '':
                msgComment = wkLine
                commentCount = commentCount + 1
            else:
                msgComment = msgComment + '\n' + wkLine
            continue

        if line[:11] == '#. Default:':
            wkLine = line[13:-2]
            defaultCount = defaultCount + 1

            if wkLine == '':
                msgDefaultSw = True
            else:
                try:
                     wkLine = wkLine.decode('utf-8')
                except Exception, em:
                    warningMsg = 'UNICODE DECODE ERROR'
                    warningRef = line[:-1] + \
                                 ', EXCEPTION: \'' + em.args[0] + '\'' + \
                                 ' codec can\'t decode byte ' + em.args[1] + \
                                 ' in position ' + \
                                  str(em.args[2]) + '-' + str(em.args[3]) + \
                                 ': ' + em.args[4]
                    warningLine =[lang, fileName, lineCount, \
                                  warningMsg, warningRef]
                    if fileWarning == [[]]:
                        fileWarning = [warningLine]
                    else:
                        fileWarning.append(warningLine)
                    warningCount = warningCount + 1
                    wkLine = '***UTF-8 DECODE ERROR***'
            msgDefault = wkLine
            continue

        if line[:4] == '#. "' and msgDefaultSw == True:
            wkLine = line[4:-2]
            try:
                wkLine = wkLine.decode('utf-8')
            except Exception, em:
                warningMsg = 'UNICODE DECODE ERROR'
                warningRef = line[:-1] + \
                             ', EXCEPTION: \'' + em.args[0] + '\'' + \
                             ' codec can\'t decode byte ' + em.args[1] + \
                             ' in position ' + \
                              str(em.args[2]) + '-' + str(em.args[3]) + \
                             ': ' + em.args[4]
                warningLine =[lang, fileName, lineCount, 
                              warningMsg, warningRef]
                if fileWarning == [[]]:
                    fileWarning = [warningLine]
                else:
                    fileWarning.append(warningLine)
                warningCount = warningCount + 1
                wkLine = '***UTF-8 DECODE ERROR***'
            msgDefault = msgDefault + wkLine

        if line[:2] == '#:':
            msgDefaultSw = False
            if msgLocations == u'':
                msgLocations = line[3:-1]
            else:
                msgLocations = msgLocations + '\n' + line[3:-1]
            continue

        if line[:8] == '#, fuzzy':
            fuzzyCount = fuzzyCount + 1
            continue

        if line[:5] == 'msgid':
            msgDefaultSw = False
            msgCommentSw = False
            serialCount = serialCount + 1
            msgCount = msgCount + 1
            msgIdLocCount = lineCount
            msgId = line[7:-2]

            if msgId == '':
                msgIdSw = True
               
            else:
                try:
                    msgId = msgId.decode('utf-8')
                except Exception, em:
                    warningMsg = 'UNICODE DECODE ERROR'
                    warningRef = line[:-1] + \
                                 ', EXCEPTION: \'' + em.args[0] + '\'' + \
                                 ' codec can\'t decode byte ' + em.args[1] + \
                                 ' in position ' + \
                                  str(em.args[2]) + '-' + str(em.args[3]) + \
                                 ': ' + em.args[4]
                    warningLine =[lang, fileName, lineCount, 
                                  warningMsg, warningRef]
                    if fileWarning == [[]]:
                        fileWarning = [warningLine]
                    else:
                        fileWarning.append(warningLine)
                    warningCount = warningCount + 1
                    msgId = u'***UTF-8 DECODE ERROR***'
                if lang == 'pot' and len(msgId) > 100:
                    warningMsg = 'MSGID IS LONGER THAN 100 CHARACTERS'
                    warningRef = 'MSGID: ' + msgId
                    warningRef = warningRef + '\n' + 'MSGLOC: ' + msgLocations
                    warningLine =[lang, fileName, lineCount, 
                                  warningMsg, warningRef]
                    if fileWarning == [[]]:
                        fileWarning = [warningLine]
                    else:
                        fileWarning.append(warningLine)
                    warningCount = warningCount + 1

        if line[:6] == 'msgstr':
            msgIdSw = False

            msgString = line[8:-2]
            if line[:9] == 'msgstr ""' and msgId == '':
                serialCount = serialCount - 1
                msgCount = msgCount -1
                msgComment = ''
                msgDefault = ''
                msgLocations = ''
                msgId = ''
                msgString = ''
                msgStringSw = False

            if line[:9] == 'msgstr ""' and msgId != '':
                msgString = u''
                msgStringSw = True

            if line[:9] != 'msgstr ""' and msgId != '':
                msgStringSw = False
                wkLine = line[8:-2]
                try:
                    msgString = wkLine.decode('utf-8')
                except Exception, em:
                    warningMsg = 'UNICODE DECODE ERROR'
                    warningRef = line[:-1] + \
                                 ', EXCEPTION: \'' + em.args[0] + '\'' + \
                                 ' codec can\'t decode byte ' + em.args[1] + \
                                 ' in position ' + \
                                  str(em.args[2]) + '-' + str(em.args[3]) + \
                                 ': ' + em.args[4]
                    warningLine =[lang, fileName, lineCount, 
                                  warningMsg, warningRef]
                    if fileWarning == [[]]:
                        fileWarning = [warningLine]
                    else:
                        fileWarning.append(warningLine)
                    warningCount = warningCount + 1
                    msgString = '***UTF-8 DECODE ERROR***'

        if line[:1] == '"':
            wkLine = line[1:-2]
            try:
                wkLine = wkLine.decode('utf-8')
            except Exception, em:
                warningMsg = 'UNICODE DECODE ERROR'
                warningRef = line[:-1] + \
                             ', EXCEPTION: \'' + em.args[0] + '\'' + \
                             ' codec can\'t decode byte ' + em.args[1] + \
                             ' in position ' + \
                              str(em.args[2]) + '-' + str(em.args[3]) + \
                             ': ' + em.args[4]
                warningLine =[lang, fileName, lineCount, 
                              warningMsg, warningRef]
                if fileWarning == [[]]:
                    fileWarning = [warningLine]
                else:
                    fileWarning.append(warningLine)
                warningCount = warningCount + 1
                wkLine = '***UTF-8 DECODE ERROR***'
            if msgStringSw == True:
                msgString = msgString + wkLine
            if msgIdSw == True:
                msgId = msgId + wkLine
                    
        if len(line) == 1 and msgId != '':
            if msgString == '':
                vacancyCount = vacancyCount + 1
            else:
                filledCount = filledCount + 1
        
            userialCount = unicode(str(serialCount))
            ulang = unicode(lang)
            umsgId = unicode(msgId)
            umsgDefault = unicode(msgDefault)
            umsgString = unicode(msgString)
            msgIdLoc = fileName + ':' + str(msgIdLocCount)
            umsgIdLoc = unicode(msgIdLoc)
            umsgLocation = unicode(msgLocations)
            umsgComment = unicode(msgComment)
            csvRec = [userialCount, ulang, ulangName, 
                      umsgIdLoc, umsgId, umsgLocation, umsgDefault, 
                      umsgString, umsgComment]
            fileCSV.append(csvRec) 

            msgComment = ''
            msgDefault = ''
            msgLocations = ''
            msgId = ''
            msgString = ''
            msgStringSw = False
            msgIdSw = False
            msgDefaultSw = False

    fileStatLine = [lang, langName, fileName,
                    lineCount, msgCount, filledCount, vacancyCount, fuzzyCount, 
                    warningCount]
    if fileWarning == [[]]:
        fileWarning = [[lang, fileName, 0, 'NO WARNING FOUND', 'NONE']]
    return fileStatLine, fileWarning, fileCSV, fileHeader

if __name__ == '__main__':
    main()

