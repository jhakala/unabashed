#!/bin/bash
ssh -t -L10121:localhost:10121 lxplus.cern.ch 'ssh -t -L10121:lxplus.cern.ch:10121 cmsusr "ssh -D10121 cmsrac31-v"'
#ssh -NL:10121:cmsrac31-v:10121 cmsusr
