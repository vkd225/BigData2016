#!/usr/bin/env python

import sys

def parseInput():
    for line in sys.stdin:
        try:
            yield line.strip('\n').split('\t')
        except:
            pass
def reducer():
    agg = {}
    for key,values in parseInput():
        print '%s,%s' % (key,values)

if __name__=='__main__':
    reducer()
