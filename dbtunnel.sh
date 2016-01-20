#!/bin/bash
ssh -t -L10121:localhost:10121 lxplus.cern.ch "ssh -L 10121:cmsrac21:10121 cmsusr"
