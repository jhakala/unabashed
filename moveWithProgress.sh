#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "Must supply the source and target directories."
  kill -INT $$
else 
  pcp ${1} ${2}
  if [ "$?" -ne 0 ]; then
    echo "lolcats."
    kill -INT $$
  else
    if [[ -d $2 ]]; then
      diff $1 $2/$1
      if [ "$?" -ne 0 ]; then
        echo "epic fail, file wuz copied but teh destination file differs from teh sauce file."
        kill -INT $$
      else
        rm -f $1
        echo "$PWD/$1 was removed."
      fi
    else 
      if [[ -f $2 ]]; then
        diff $1 $2
        if [ "$?" -ne 0]; then
          echo "noobsauce -- file wuz copied but the destination file differs from teh sauce file."
          kill -INT $$
        else
          rm -f $1
          echo "$PWD/$1 was removed."
        fi
      fi
    fi
  fi
fi
if [ "$?" -ne 0 ]; then
  echo "all your base are belong to teh fail"
else
  echo "Moving succeeded."
fi  

