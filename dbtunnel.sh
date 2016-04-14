#!/bin/bash
if [ $1 = "outside" ]; then
	echo "this might not work yet..."
	#ssh lxplus.cern.ch -L10121:localhost:10121 'ssh -L:10121:cmsrac31-v:10121 cmsusr.cern.ch'
	ssh -Y -t -f lxplus.cern.ch -L10121:localhost:10121 "ssh -Y -NL10121:cmsrac31-v:10121 cmsusr" 
elif [ $1 = "cern" ]; then
	ssh -Y -NL:10121:cmsrac31-v:10121 cmsusr.cern.ch
fi
