#!/bin/bash
for i in `condor_q | grep ' R ' | awk {'print $1'} `; do echo ${i} ; condor_tail ${i} ; condor_tail ${i} -stderr; echo -e "\n------------------------------------\n\n"; done
