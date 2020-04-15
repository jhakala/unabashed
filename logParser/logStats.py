from sys import argv
from os.path import exists
from commands import getoutput
import operator
import json
 
# John Hakala 8/8/17

# Example usage:
# johakala@lxplus067 ~/unabashed/logParser # javac logParser.java
# johakala@lxplus067 ~/unabashed/logParser # python logStats.py ~/log1.xml

if len(argv) != 2:
  print "please supply one argument, the input log file"
  exit(1)

if not exists("logParser.class"):
  print "logParser has not been compiled."
  print "please run:"
  print "javac logParser.java"
  exit(1)

inputLog = argv[1]
# call the java program -- python is too slow for big logfiles
fromJava = getoutput("java logParser %s" % inputLog)
# turn the JSON into a dict
statsDict =  json.loads(fromJava)

# sort them and print them prettily
sortedStats = sorted(statsDict.items(), key=operator.itemgetter(1), reverse=True) 
print "{0: <45} {1: >8}".format("Written by", "# logs")
for stat in sortedStats:
  print "{0: <45} {1: >8}".format(stat[0], stat[1])
