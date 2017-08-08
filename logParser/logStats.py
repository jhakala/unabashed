from sys import argv
from commands import getoutput
import operator
from pprint import pprint
import json
 
inputLog = argv[1]
fromJava = getoutput("java logParser %s" % inputLog)
#fromJava ='{"test":2}'
statsDict =  json.loads(fromJava)


sortedStats = sorted(statsDict.items(), key=operator.itemgetter(1), reverse=True) 
print "{0: <45} {1: >8}".format("Written by", "# logs")
for stat in sortedStats:
  print "{0: <45} {1: >8}".format(stat[0], stat[1])
