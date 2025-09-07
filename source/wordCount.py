#!/usr/local/bin/python3

import os
import sys
import re

# INIT
wordList = {}
data = b""
buffer = ""
loopCounter = 1

if len(sys.argv) < 3:
    print("wordCount: invalid args\n"
          + "usage: wordCount [input file...] [output file...]")
    exit(1)

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

print("INPUT: %s\nOUTPUT: %s" % (inputFileName, outputFileName))

inputFD = os.open(inputFileName, os.O_RDONLY)
print("Reading Input")

while True:
    data = os.read(inputFD, 1024)  # 1KB at a time
    if not data:
        break  # EOF

    print(str(loopCounter) + "KB read")
    loopCounter += 1

    buffer += data.decode("utf-8")
    line = re.findall(r"\w+", buffer.lower())

    # handle partial words at end of buffer
    if buffer[-1].isalpha():
        buffer = line[-1]
        del line[-1]
    else:
        buffer = ""

    for word in line:
        if word not in wordList:
            wordList[word] = 1
        else:
            wordList[word] += 1


os.close(inputFD)
print("Input Closed")

keyOrder = list(wordList.keys())
keyOrder.sort()
outputFD = os.open(outputFileName, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
print("Writing Output")

for word in keyOrder:
    entry = "%s %d\n" % (word, wordList[word])
    data = entry.encode('utf-8')
    os.write(outputFD, data)

os.close(outputFD)
print("Output closed")
