#!/bin/bash
expect -c 'eval spawn ssh -t -f lxplus.cern.ch -L1081:localhost:1081 "ssh -t -f -ND 1081 cmsusr" &; interact'
expect -c 'eval spawn ssh -t -f lxplus.cern.ch -L1080:localhost:1080 "ssh -t -f -ND 1080 cms904usr" &; interact'
