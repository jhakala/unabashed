#!/bin/bash
for i in `condor_q $1 | grep ' R ' | awk {'print $1'} `; do echo ${i} ; timeout 5 condor_tail ${i} ; timeout 5 condor_tail ${i} -stderr; echo -e "\n------------------------------------\n\n"; done
