#!/usr/bin/python

import pycurl
import sys
import getopt
from StringIO import StringIO
import json

class MtGCard:
    price = 0.00
    name = ""
    setName = ""

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def main(argv):
    buffer = StringIO()
    #generate urls
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"v:",["verbose="])
    except getopt.GetoptError:
        print 'parse.py -v <verbose>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'parse.py -p <pages> -u <user> -v <verbose>'
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose = str2bool(arg)

    # This is the main code.  Everything above this is just parsing user input.

    c = pycurl.Curl()
    c.setopt(c.URL, "http://www.mtgprice.com/magic-the-gathering-prices.jsp")
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()

    sets = []
    setSplits = body.split("/spoiler_lists/")
    for setFound in range(1, len(setSplits)):
        parsedSet = setSplits[setFound].split("\"")[0]
        if verbose:
            print ("Found set {0}".format(parsedSet))
        sets.append(parsedSet)
        if "Zendikar_Expeditions" in parsedSet:
            break

    cardPrices = []
    # for foundSet in range(0, len(sets)):
    for foundSet in range(0, len(sets)):
        try:

            buffer = StringIO()
            currSet = sets[foundSet]
            if verbose:
                print currSet
            if "Foil" in currSet:
                continue
            c = pycurl.Curl()
            c.setopt(c.URL, "http://www.mtgprice.com/spoiler_lists/{0}".format(currSet))
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()

            cardSplit = body.split("$scope.setList =  ")[1].split(";")[0]

            if verbose:
                print cardSplit

            setCards = json.loads(cardSplit)
            for cardNumber in range(0, len(setCards)):
                try:

                    price = float(setCards[cardNumber]['bestVendorBuylistPrice'])
                    if price > 0:
                        if "U" in setCards[cardNumber]['rarity']:
                            print "{0},U,{1},{2}".format(setCards[cardNumber]['setName'], setCards[cardNumber]['name'], setCards[cardNumber]['bestVendorBuylistPrice'])
                        if "C" in setCards[cardNumber]['rarity']:
                            print "{0},C,{1},{2}".format(setCards[cardNumber]['setName'], setCards[cardNumber]['name'], setCards[cardNumber]['bestVendorBuylistPrice'])
                except:
                    if verbose:
                        print("Unexpected error:", sys.exc_info()[0])
            if verbose:
                print "Parsed {0}".format(currSet)
        except:
            print("Unexpected error with {0}:{1}".format(currSet, sys.exc_info()[0]))
if __name__ == "__main__":
   main(sys.argv[1:])
