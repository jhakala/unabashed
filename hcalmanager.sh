#!/bin/bash
# Usage: ./hcalmanager.sh <database name>
# The database name can be either 'p5', '904', or 'omds'
# You will also need to have hcalmanager.jar, RSMANAGER.p5.properties, RSMANAGER.904.properties, and RSMANAGER.omds.properties in your home directory
# Example: ./hcalmanager.sh omds
if [ "$1" = "p5" ] || [ "$1" = "904" ] || [ "$1" = "omds" ] ; then
  echo "Launching hcalmanager for the $1 database"
  rm -f RSMANAGER.properties
  cp ~/RSMANAGER.${1}.properties ~/RSMANAGER.properties
  /Library/Java/JavaVirtualMachines/1.7.0.jdk/Contents/Home/bin/java -jar hcalmanager.jar
  # You may need to change the above line to point to where your java 7 jdk or jre's directory
else
  echo "Please run hcalmanager.sh with one of the following options for selecting an RS database: 'p5', '904', or 'omds'"
fi
