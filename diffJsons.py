import json
from sys import argv
from os.path import basename, exists, isfile
# for diffing golden JSONs
# JCH 1/29/21

# check args
if not len(argv) == 3:
  print "must supply two json filenames as arguments"
  exit(1)
fail = False
if not exists(argv[1]):
  print "file does not exist:", argv[1]
  fail = True
if not exists(argv[2]):
  print "file does not exist:", argv[2]
  fail = True
if fail:
  print "exiting"
  exit(1)

# open JSONs
filea = open(argv[1])
fileb = open(argv[2])

print "comparing %s and %s" % (filea.name, fileb.name)

# parse jsons
# these should give an error if the json isn't valid
jsona = json.load(filea)
jsonb = json.load(fileb)

# this lambda function gives the set of things (runs) in either list (the list of json keys) 
# that are not in the other list. i.e. the complement of the intersection of the two lists
compl_inter = lambda x, y: list((set(x)- set(y))) + list((set(y)- set(x)))
 
# find all runs that are in one but not both jsons
non_match = compl_inter(jsona.keys(), jsonb.keys())
if len(non_match) != 0:
  print "not matching runs:", [int(i) for i in non_match]
 
# find all runs present in both but don't contain the same lumisections
messups = []
for key in jsona.keys():
  if not key in non_match:
    if not key in jsonb.keys():
      # i don't think this should ever be reached, but alert if so
      print "run %s is not in", jsonb.keys()
    if jsona[key] == jsonb[key]:    # if the lumis match, OK
      continue
    else:                           # but if they don't, there is a problem
      messups.append((key,(jsona[key], jsonb[key])))

for messup in messups:
  # this messages would print out all lumis for runs that have a problem
  #print "       ",  basename(filea.name)
  #print "           ", messup[1][0]
  #print "       ",  basename(fileb.name)
  #print "           ", messup[1][1]

  # instead of printing all the lumis in runs with a problem, just find the specific
  # lumis in each run which don't match
  speca = messup[1][0]
  specb = messup[1][1]
  for x in reversed(speca): # the reverse is needed to remove things while iterating
    if x in specb:
      speca.remove(x)
      specb.remove(x)
  for x in reversed(specb):
    if x in speca:
      specb.remove(x)

  # print out all the lumiblocks which don't match
  print "not matching lumis within run", messup[0], ":"
  print "       ",  basename(filea.name)
  print "           ", speca
  print "       ",  basename(fileb.name)
  print "           ", specb
  
if len(non_match) == 0 and len(messups) == 0:
  print "\nJSONs match!"
