#!/usr/bin/env python


from operator import itemgetter
import sys

currentKey = None
currentCount = 1
currentPercentageTotal = 0.0
Key = None
for line in sys.stdin:
    if line is not None:
        line = line.strip()
        data = line.split('\t')
        value = data[1]
        Key = data[0]
        if currentKey == Key and "CSH" not in value:
            currentCount += 1
            percentage = float(value.split(",")[0])
            currentPercentageTotal += percentage
        else:
            if currentKey:
                result = str(currentPercentageTotal/currentCount)
                print "%s , %s" % (currentKey, result)
            currentKey = Key
            if "CSH" not in value:
                currentCount = 1
                currentPercentageTotal = float(value.split(",")[0])
if currentKey == Key:
    result = str(currentPercentageTotal/currentCount)
    print "%s , %s" % (currentKey, result)
