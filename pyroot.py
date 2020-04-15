# for bashrc:
# alias pyroot="python -i ~/unabashed/pyroot.py"
from sys import argv
from ROOT import *
tfile=[]
i=0
for fileName in argv[1:]:
  tfile.append(TFile(str(fileName)))
  print "Opened %s as 'tfile[%i]'" % (fileName, i)
  tfile[-1].ls()
  i += 1
