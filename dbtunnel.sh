#!/bin/bash
# this is for connecting to the RSDB for p5 or 904 from either inside CERN or outside
# usage: ./dbtunnel.sh outside cms
# John Hakala 4/14/2016
if [ $# -ne 2 ]; then
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
  exit 1
fi

if [ $2 = "cms" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f johakala@lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:cmsrac42-v:10121 cmsusr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL:10121:cmsrac31-v:10121 cmsusr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
elif [ $2 = "904" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f johakala@lxplus.cern.ch -L10122:localhost:10122 "ssh -Y -NL10122:int2r1-v.cern.ch:10121 cms904usr" 
	elif [ $1 = "cern" ]; then
		ssh -Y -f -NL10122:int2r1-v.cern.ch:10121 cms904usr.cern.ch
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
elif [ $2 = "omds" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f -NL3307:itrac5115.cern.ch:5529 johakala@lxplus.cern.ch
	elif [ $1 = "cern" ]; then
    echo "You don't need a tunnel for omds if you're on the CERN GPN."
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
elif [ $2 = "fnal" ]; then
	if [ $1 = "outside" ]; then
		ssh -Y -f -NL3310:cmsnghcal01:3306 jhakala@cmslpc30.fnal.gov
	elif [ $1 = "cern" ]; then
    echo "Use 'outside' instead of 'cern' for FNAL."
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
elif [ $2 = "tifr" ]; then
	if [ $1 = "outside" ]; then
    ssh -NL3311:localhost:3306 camac@158.144.55.7
	elif [ $1 = "cern" ]; then
    echo "Use 'outside' instead of 'cern' for TIFR."
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
elif [ $2 = "hcalrcmsdev" ]; then
	if [ $1 = "outside" ]; then
		#ssh -Y -f -NL3312:cmshcal24:3306 johakala@lxplus.cern.ch
		ssh -Y -f johakala@lxplus.cern.ch -L3312:localhost:3306 "ssh -Y -NL3306:localhost:3306 cmshcal24" 
	elif [ $1 = "cern" ]; then
    echo "Use 'outside' instead of 'cern' for hcalrcmsdev."
  else
    echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
    exit 1
	fi
else
  echo "Please run dbtunnel with two options. The first can be 'outside' or 'cern', and the second can be 'cms', '904',  'omds', 'fnal', 'hcalrcmsdev', or 'tifr'"
  exit 1
fi
