# for bashrc:
# alias pyroot="python -i ~/unabashed/pyroot.py"
from sys import argv
from ROOT import *
tfile = TFile(argv[1])
print "Opened %s as 'tfile'"%argv[1]
tfile.ls()
