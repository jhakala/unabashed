#!/bin/bash
# Script for tunnelling into the cms network
# Usage: unabashed/tunnel.sh cern
# The option can be either 'cern' or 'outside' depending on whether you're on the CERN gpn already or not
# John Hakala 4/20/2016
if [ "$#" -ne 1 ];then
  echo "Please run tunnel.sh with one option: either 'outside' or 'cern'"
  exit 1
fi

if [ "$1" = "outside" ]; then
  expect -c 'eval spawn ssh -Y -f johakala@lxplus.cern.ch -L1081:localhost:1081 "ssh -f -ND 1081 cmsusr" &; interact'
  expect -c 'eval spawn ssh -Y -f johakala@lxplus.cern.ch -L1080:localhost:1080 "ssh -f -ND 1080 cms904usr" &; interact'
elif [ "$1" = "cern" ]; then
  expect -c 'eval spawn ssh -f -ND 1081 cmsusr.cern.ch &; interact'
  expect -c 'eval spawn ssh -f -ND 1080 cms904usr.cern.ch &; interact'
else
  echo "Please run tunnel.sh with one option: either 'outside' or 'cern'"
  exit 1
fi
