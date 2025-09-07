#!/usr/local/bin/python3

import os
import sys
import re

wordList = {}
data = b""
buffer = ""
loopCounter = 1

inputFileName = sys.argv[0]
outputFileName = sys.argv[1]

inputFD = os.open(inputFileName, os.O_RDONLY)
print("Reading Input\n")

while True:
    data = os.read(inputFD, 1024)  # 1MB at a time
    if not data:
        break  # EOF

    print(str(loopCounter) + "MB read\n")
    loopCounter += 1

    buffer += data.decode("utf-8")
    line = re.findall(r"\w+", buffer)

    buffer = line[-1]
    line[-1] = ''

    for word in line:
        if word not in wordList:
            wordList[word] = 1
        else:
            wordList[word] += 1


os.close(inputFD)
print("Input Closed\n")

print(wordList.keys())

keyOrder = list(wordList.keys())
keyOrder.sort()
outputFD = os.open(outputFileName, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
print("Writing Output\n")

for word in keyOrder:
    entry = "%s %d\n" % (word, wordList[word])
    data = entry.encode('utf-8')
    os.write(outputFD, data)

os.close(outputFD)
print("Output closed\n")
