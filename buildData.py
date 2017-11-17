#!/usr/bin/python

import pycurl
import sys
import getopt
from StringIO import StringIO

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

    # for foundSet in range(0, len(sets)):
    for foundSet in range(0, 1):
        currSet = sets[foundSet]
        if verbose:
            print currSet
        c = pycurl.Curl()
        c.setopt(c.URL, "http://www.mtgprice.com/spoiler_lists/{0}".format(currSet))
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        print "Parsed {0}".format(currSet)

        
if __name__ == "__main__":
   main(sys.argv[1:])
