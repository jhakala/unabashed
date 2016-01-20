#!/bin/bash
expect -c 'eval spawn ssh -f -ND 1081 cmsusr.cern.ch &; interact'
expect -c 'eval spawn ssh -f -ND 1080 cms904usr.cern.ch &; interact'
