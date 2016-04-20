#!/bin/bash
# this is for connecting to the RSDB for p5 or 904 from either inside CERN or outside
# usage: ./dbtunnel.sh outside cms
# John Hakala 4/14/2016
if [ $# -ne 2 ]; then
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms' or '904'"
  exit 1
fi

if [ $2 = "cms" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -t -f lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:cmsrac31-v:10121 cmsusr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL:10121:cmsrac31-v:10121 cmsusr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms' or '904'"
    exit 1
	fi
elif [ $2 = "904" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -t -f lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:int2r1-v.cern.ch:10121 cms904usr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL10121:int2r1-v.cern.ch:10121 cms904usr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms' or '904'"
    exit 1
	fi
else
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms' or '904'"
  exit 1
fi
