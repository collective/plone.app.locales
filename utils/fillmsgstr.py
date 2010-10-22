#!/usr/bin/env python
# encoding: utf-8

#  fillmsgstr.py
#  Created by Russ Ferriday 2006.03.28
#  http://topia.com
#  Copyright (c) 2006 Russ Ferriday - russf@topia.com
#
#  This program is dedicated to Rhoslyn Prys and Emyr Thomas...
#     Welcome to Plone! And thank you for Plone in Welsh!
#
#  Licenced under the FreeBSD licence:
#  http://www.freebsd.org/copyright/freebsd-license.html
#  (i.e. do with it what you want but keep this notice.)

import os
import sys
import getopt
import fileinput

help_message = '''
fillmsgstr [-h] [-r] [-v] [-o] <inputFile1> [ <inputFile2> [<inputFile3> ... ] ]
  -h : print this text
  -r : reverse the process
  -v : verbose -- a good way to get just the messages
  -o : output file -- defaults to <inputFile>.filled - Only works with single input file.
  <inputFile> : the file(s) you want to process or reverse process

  'Processing' takes the contents of all Default lines, and copies them
  into msgid lines, as a starting point for Translation Memory enabled tools.
  The previous contents of msgid being saved as #savedmsgid

  'Reverse Processing' renames #savedmsgid to msgid, and deletes the next msgid.

  So an example from the end of plone.po looks like this:

#. Default: "You are here:"
#: ./skins/plone_templates/global_pathbar.pt
msgid "you_are_here"
msgstr ""

  After running fillmsgstr.py on the plone.po file, the last entry will look like this in
  the newly created plone.po.filled.

#. Default: "You are here:"
#: ./skins/plone_templates/global_pathbar.pt
#savedmsgid "you_are_here"
msgid "You are here:"
msgstr ""

  Notice that the msgid, "you_are_here", has been relabeled #savedmsgid and
  the Default: value has been put in its place.

  Then the file is run through a translation tool. It's probably useful to
  rename the plone.po.filled file to plone.po before this, so the extension
  meets expectations. If the tool has a translation memory the english value
  of the msgid, "You are here:" is used as the lookup key. You can see how a
  msgid of "you_are_here" might not occur much in literature and would not be
  automatically translated by a TM tool.

#. Default: "You are here:"
#: ./skins/plone_templates/global_pathbar.pt
#savedmsgid "you_are_here"
msgid "You are here:"
msgstr "Sie sind hier:"

  So finally we run fillmsgstr.py with the -r option, giving the plone.po file
  as the input file. The last entry in the resulting plone.po.unfilled file
  will look like this:

#. Default: "You are here:"
#: ./skins/plone_templates/global_pathbar.pt
msgid "you_are_here"
msgstr "Sie sind hier:"

  Notice that the original msgid has been replaced, and the savedmsgid has
  been removed.

  Copyright (c) 2006 Russ Ferriday - russf@topia.com
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def dump(s):
    print '>>> %s' % s

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hro:v",
                                       ["help", "output="])
        except getopt.error, msg:
             raise Usage(msg)

        # option processing
        verbose, output, infile, infilepath, reverse = \
          False, None, None, None, False
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-r"):
                reverse = True
        if len(args) < 1:
            print >> sys.stderr, "You forgot your input file..."
            raise Usage(help_message)

        if len(args) > 1 and output:
            print >> sys.stderr, "If you specify an output file, then you may only provide a single input file..."
            raise Usage(help_message)


        for infilepath in args:
            if os.path.isfile(infilepath):
                infile=fileinput.input(infilepath)
            else:
                print >> sys.stderr, "Check your input file. %s Is it a text file?" % infilepath
                raise Usage(help_message)

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    for infilepath in args:
        infile=fileinput.input(infilepath)

        if output:
            outfilepath=output
        else:
            if reverse:
                outfilepath=infilepath + '.unfilled'
            else:
                outfilepath=infilepath + '.filled'

        outfile=open(outfilepath, 'w')

        defMark='#. Default:'
        msgidMark='msgid '
        msgstrMark='msgstr '
        savedMark='#saved'
        buff = None
        if reverse:
            for line in infile:
                # convert the #savedmsgid lines back to msgid lines
                # and swallow the next msgid, i.e. the fake one we created earlier
                if line.startswith(savedMark):
                    buff=1
                    # save this line, less the savedMark, until we see the msgstr line
                    delayedLine=line[len(savedMark):]
                    continue
                if not buff:
                    outfile.write(line)
                    continue
                # ok, so we're buffering, which means...
                #   Delete next msgid, by omission, and drop the delayedLine in its place.
                #   This ensures it appears after any comments that it may been
                #   moved ahead of by some translation memory tools.
                if line.startswith(msgidMark):
                    buff=None
                    outfile.write(delayedLine)
                    continue
                # but meanwhile other lines remain unchanged
                outfile.write(line)
        else:
            for line in infile:
                if line.startswith(defMark):
                    buff=line[len(defMark):]
                    outfile.write(line)
                    continue
                if not buff:
                    outfile.write(line)
                    continue
                # ok, so we're buffering, which means...

                # we rename msgid to savedmsgid
                # and if the msgid is cryptic (different from buff) write buff
                # as msgid, else write line
                if line.startswith(msgidMark):
                    outfile.write('#saved%s' % line)
                    if line[len(msgidMark):] <> buff:
                        oline='msgid%s' % buff
                    else:
                        oline=line
                    outfile.write(oline)
                    buff=None
                    if verbose:
                        dump(oline)
                    continue
                outfile.write(line)

        outfile.close()
        infile.close()


if __name__ == "__main__":
    sys.exit(main())
