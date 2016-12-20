#!/bin/bash
# this is for connecting to the RSDB for p5 or 904 from either inside CERN or outside
# usage: ./dbtunnel.sh outside cms
# John Hakala 4/14/2016
if [ $# -ne 2 ]; then
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904', or 'omds'"
  exit 1
fi

if [ $2 = "cms" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:cmsrac31-v:10121 cmsusr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL:10121:cmsrac31-v:10121 cmsusr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904', or 'omds'"
    exit 1
	fi
elif [ $2 = "904" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f lxplus.cern.ch -L10122:localhost:10122 "ssh -Y -NL10122:int2r1-v.cern.ch:10121 cms904usr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL10122:int2r1-v.cern.ch:10121 cms904usr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904', or 'omds'"
    exit 1
	fi
elif [ $2 = "omds" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f -NL3307:cmshcalweb01.cern.ch:3306 lxplus.cern.ch
	elif [ $1 = "cern" ]; then
    echo "You don't need a tunnel for omds if you're on the CERN GPN."
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904', or 'omds'"
    exit 1
	fi
else
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904', or 'omds'"
  exit 1
fi
