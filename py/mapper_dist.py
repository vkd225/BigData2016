#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    data = line.split(",")
    try:
        paymentType = data[13]
        key = data[8]
        payment = float(data[19])
        tip = float(data[17])
    except ValueError:
        pass
    if payment != 0:
        percentage = tip*100/payment
    else:
        percentage = 0
    value = str(percentage) + "," + paymentType
    print '%s\t%s' % (key, value)
