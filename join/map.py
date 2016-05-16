#!/usr/bin/env python

import sys

# header=0 if headers are present
header = 1
for line in sys.stdin:
    if header == 0:
        header = 1
        continue
    line = line.strip()
    splits = line.split(",")

    # if and elif ensures that only the tuples that have all the entries will be accepted, we will remove other tuples
    if len(splits) == 11:
        print "%s,%s,%s,%s\t%s,%s,%s,%s,%s,%s,%s,%s" % (
            splits[0], splits[1], splits[2], splits[3], "0", splits[4], splits[5], splits[6], splits[7], splits[8],
            splits[9], splits[10])
    elif len(splits) == 14:
        print "%s,%s,%s,%s\t%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            splits[0], splits[1], splits[2], splits[5], "1", splits[3], splits[4], splits[6], splits[7], splits[8],
            splits[9], splits[10], splits[11], splits[12], splits[13])
