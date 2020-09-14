#!/bin/bash
for i in `condor_q $1 | grep ' R ' | awk {'print $1'} `; do echo ${i}  `condor_q ${i} -l -af MachineAttrGLIDEIN_CMSSite0 | xargs | awk '{print $6}'; echo`; done 
