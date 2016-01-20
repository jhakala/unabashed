#!/bin/bash
source /cvmfs/cms.cern.ch/crab3/crab.sh
echo "This is my silly hack for monitoring my crab jobs, Nov 19" 
while :
do
  
	cd /afs/cern.ch/work/j/johakala/public/CMSSW_7_4_14/src/BH/BHAnalysis/crab_jobs_2015DreMiniAOD05Oct2015v1_Nov27/crab_BHnTuples_201§5DreMiniAOD05Oct2015v1_Nov2
  date
  crab status $PWD
  sleep 20
  cd /afs/cern.ch/work/j/johakala/public/CMSSW_7_4_14/src/BH/BHAnalysis/crab_jobs_2015DpmptRecoV4_Nov27/crab_BHnTuples_2015DpmptRecoV4_Nov27
  date
  crab status $PWD
  sleep 20
done  
