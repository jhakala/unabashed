#!/bin/bash
# Script that does a cp, but it gives you progress while it's copying.
# John Hakala, 1/20/2016 (but written a while ago)
if [ "$#" -ne 2 ]; then
  echo "inb4 you forgot teh sauce and target directories."
  kill -INT $$
else 
  filename=$(basename $1)
  if [[ -d $2 ]]; then
    if [[ -f ${2}/${filename} ]]; then
      echo "${2}/${filename} already exists, lulz."
      kill -INT $$
    else
      echo "Copying ${filename} to directory $2"
      rsync -ah --progress $1 ${2}/${filename}
      if [ "$?" -ne 0 ]; then
        echo "copying got pwned."
        kill -INT $$
      else
      echo "Copy succeeded."
      fi
    fi
  else
    if [[ -f $2 ]]; then
      echo "$2 already exists, nub. Use fpcp to force overwrite it."
      kill -INT $$
    else
      echo "Copying ${filename} to $2"
      rsync -ah --progress $1 ${2}
      if [ "$?" -ne 0 ]; then
        echo "Copy wuz teh fail."
        kill -INT $$
      else
      echo "Copy succeeded."
      fi
    fi
  fi
fi
