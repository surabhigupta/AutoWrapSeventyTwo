#!/usr/bin/python

import sys

message_file = sys.argv[1]
debug = False

def wrapCommitMessageTo72CharsPerLine(message):
    """
    Given a commit message, add line breaks at appropriate places such that 
    no message is more than 72 characters wide.
    Exception: URLs or other long strings that are more than 72 characters wide (since these cannot be broken up)

    The algorithm below tracks the position of one previous whitespace character and maintains
    a running count of characters since last new line. After the count exceeds 72, the next whitespace
    is converted into a new line character \r\n (carriage return/line feed) 

    Existing line breaks are left as-is, as are any lines that are less than 72 characters long.
    """

    #The formatted commit message
    commit_msg = ""

    #Going through all the lines in the commit message, one line at a time
    for lineno, line in enumerate(message):
        characterCountSinceNewLine = 0;
        lastWhiteSpace=0

        for index in range(0, len(line)):
            commit_msg += line[index]
            characterCountSinceNewLine += 1
            if (debug) :
                print "Character: " + str(line[index]) + " count: " + str(characterCountSinceNewLine)
            if line[index].isspace():
                if characterCountSinceNewLine > 72 and lastWhiteSpace > 0:
                    if (debug) :
                        print "Inserting a new line after previous word " + str(index-lastWhiteSpace+1) + " characters ago."
                        print "Resetting character count since last new line to " + str(index - lastWhiteSpace)
                    commit_msg = replaceWhiteSpaceWithNewLine(commit_msg, -(index-lastWhiteSpace+1))
                    characterCountSinceNewLine = index-lastWhiteSpace
                #last white space is updated
                lastWhiteSpace=index;
    return commit_msg

# Helper method to replace the whitespace with new line character
# at specific positions in the commit message. Note the usage of 
# negative indices for better readability and accuracy (in cases
# where the length of the commit message was modified)

def replaceWhiteSpaceWithNewLine(commit_Message, position) :
    if not commit_Message[position].isspace():
        print "Warning: White space expected at position " + str(position)
    
    #A new line character is added at the specified position
    result = commit_Message[:position] + '\r\n' 
    if (position !=-1):
        result += commit_Message[(position+1):] 
    
    return result

#Process original commit message
with open(message_file) as originalCommit:
    formatted_commit_msg = wrapCommitMessageTo72CharsPerLine(originalCommit)

#Write formatted commit message
with open(message_file, 'w') as formattedMessageFile:
    formattedMessageFile.write(formatted_commit_msg)


