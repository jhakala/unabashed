#!/bin/bash
# temporary hack for generating html since altair's 
# auto-generated html is broken for me
if [ ! -d "outputHTML" ]; then
  mkdir outputHTML
fi
JSONS=$( ls -1v outputPlots )
NAMES=$( for JSON in ${JSONS[@]}; do echo $JSON | sed 's/.json//g'; done )
for NAME in ${NAMES[@]}; do cat header.html > outputHTML/${NAME}.html; cat outputPlots/${NAME}.json >> outputHTML/${NAME}.html; cat footer.html >> outputHTML/${NAME}.html; done
