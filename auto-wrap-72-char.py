#!/usr/bin/python

from __future__ import print_function
import codecs

import sys

debug = False


def info(message):
    if debug:
        print(message, file=sys.stderr)
        sys.stderr.flush()


def wrapCommitMessageToAMaxWidth(originalMessage, maxWidth=72, linesep='\n'):
    """
    Given a commit message, add line breaks at appropriate places such that no line
    in the message is more than 72 characters wide.

    :param originalMessage:
    :param linesep: line separator that is inserted into the message
    :param message: a file object representing the commit message
    :param maxWidth: the maximum width for the message

    Exception: URLs or other long strings that are more than 72 characters wide
    (since these cannot be broken up)

    The algorithm below tracks the position of one previous whitespace character
    and maintains a running count of characters since the last new line. If the count
    exceeds 72, the next whitespace is replaced by a (os-specific) line separator

    Existing line breaks are left as-is, as are any lines that are less than 72 characters long.
    Note: There exists a "textwrap" library python that will wrap commit messages
    to a specified width. However, it truncates in the middle of an url (or a long string)
    if its length is more than the max width. I welcome any suggestions and/or contributions
    around performance improvements.
    """

    #The formatted commit message
    commit_msg = []
    # Helper method to replace the whitespace at specific positions in the
    # last line of the commit message with a new line character.
    # The last element of the commit_msg array is replaced by the two elements,
    # the first of which ends with a line separator


    def replaceWhiteSpaceWithNewLine(position):
        currentLine = commit_msg.pop()
        
        #Throw warning if white space is being inserted within the boundaries
        #of contiguous text
        if not currentLine[position-1].isspace():
            info("Warning: White space expected at position %d %s" % (position, currentLine[position]))

        #White space is replaced by a new line character at the specified position   
        commit_msg.append(currentLine[:(position-1)] + linesep)
        commit_msg.append(currentLine[position:])

    #Going through all the lines in the commit message, one line at a time
    for lineno, line in enumerate(originalMessage):
        characterCountSinceNewLine = 0
        lastWhiteSpace = 0
        commit_msg.append(line)
        
        if line.startswith("#"):
            continue

        for index, ch in enumerate(line):
            characterCountSinceNewLine += 1
            if ch.isspace():
                info("Character count since last new line: %d" % characterCountSinceNewLine)
                if characterCountSinceNewLine > (maxWidth + 1) and lastWhiteSpace > 0:
                    replaceWhiteSpaceWithNewLine(lastWhiteSpace)
                    characterCountSinceNewLine = (characterCountSinceNewLine - lastWhiteSpace)
                    lastWhiteSpace = 0
                    info("Inserting a new line after previous word:%s (%d characters ago)" %
                         (line[lastWhiteSpace:characterCountSinceNewLine], characterCountSinceNewLine))
                    info("Resetting character count since last new line to %d" % characterCountSinceNewLine)

                #last white space is updated
                lastWhiteSpace = characterCountSinceNewLine

    return ''.join(commit_msg) 

# 
# Begin main method
#


def main(args):
    message_file = args[1]
    #Process original commit message
    with codecs.open(message_file, 'rb', encoding='utf-8') as originalCommit:
        formatted_commit_msg = wrapCommitMessageToAMaxWidth(originalCommit)

    #Write formatted commit message
    with codecs.open(message_file, 'wb', encoding='utf-8') as f

#
# End main method
#

if __name__ == '__main__':
    try :
        main(sys.argv)
    except Exception as e:
        print("Something bad happened while executing the main() method")
        sys.exit(1)
