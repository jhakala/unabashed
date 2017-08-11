from sys import argv
from os.path import exists
from commands import getoutput
import operator
import json
from copy import deepcopy
from john_emapParser import emapper
 
# John Hakala 8/8/17

# Example usage:
# johakala@lxplus067 ~/unabashed/logParser # javac logParser.java
# johakala@lxplus067 ~/unabashed/logParser # python logStats.py ~/log1.xml

if len(argv) != 2:
  print "please supply one argument, the input xml dir"
  exit(1)

if not exists("testParser.class"):
  print "logParser has not been compiled."
  print "please run:"
  print "javac testParser.java"
  exit(1)

inputDir = argv[1]
# call the java program -- python is too slow for big logfiles
fromJava = getoutput("java testParser %s" % inputDir)
# turn the JSON into a dict
ampsDict =  json.loads(fromJava)


emap = emapper("HCALmapHBHElegacy_J.txt")
emap.parseEmap()

hcalDict = deepcopy(emap.search({}))
for channel in hcalDict:
  channel["amplitude"] = ampsDict[channel["rbx"]]

# sort them and print them prettily
print "{0: <8} {1: <8} {2: <8} {3: >8}".format("ieta", "iphi", "depth", "amplitude")
print "{0: <8} {1: <8} {2: <8} {3: >8}".format("----", "----", "-----", "---------")
for channel in hcalDict:
  print "{0: <8} {1: <8} {2: <8} {3: >8}".format(channel["eta"], channel["phi"], channel["depth"], channel["amplitude"])
