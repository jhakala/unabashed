#!/bin/bash
# this is for connecting to the RSDB for p5 from either inside CERN or outside
# usage: ./dbtunnel.sh outside
# John Hakala 4/14/2016
if [ $1 = "outside" ]; then
	ssh -Y -t -f lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:cmsrac31-v:10121 cmsusr" 
elif [ $1 = "cern" ]; then
	ssh -Y -NL:10121:cmsrac31-v:10121 cmsusr.cern.ch
fi
