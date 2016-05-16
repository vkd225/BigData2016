#!/usr/bin/env python
import sys

trips = []
fares = []
prevKey = ""
key = ""
init = 0

for line in sys.stdin:
    prevKey = key
    key, valuelist = line.strip().split("\t", 1)

    if init == 0:
        init = 1
        prevKey = key

    try:
        value = valuelist.split(",")
        # print "%s" % (value[0])
        if int(value[0]) == 1:
            # print "%s?%s" % (key,valuelist)
            trips.append(key + "?" + valuelist)
        else:
            # print "%s()%s" % (key,valuelist)
            fares.append(key + "?" + valuelist)
    except ValueError:
        continue

    if prevKey != key:
        for trip in trips:
            keyTrip, valueTrip = trip.split("?", 1)
            for fare in fares:
                keyFare, valueFare = fare.split("?", 1)
                if keyTrip == keyFare:
                    tempTrip = valueTrip.split(",")
                    stringTrip = tempTrip[1:]
                    tempFare = valueFare.split(",")
                    stringFare = tempFare[1:]
                    print "%s\t%s,%s" % (keyTrip, ",".join(stringTrip), ",".join(stringFare))
        trips = trips[len(trips) - 1:]
        fares = fares[len(fares) - 1:]

for trip in trips:
    keyTrip, valueTrip = trip.split("?", 1)
    for fare in fares:
        keyFare, valueFare = fare.split("?", 1)
        if keyTrip == keyFare:
            tempTrip = valueTrip.split(",")
            stringTrip = tempTrip[1:]
            tempFare = valueFare.split(",")
            stringFare = tempFare[1:]
            print "%s\t%s,%s" % (keyTrip, ",".join(stringTrip), ",".join(stringFare))
