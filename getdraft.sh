#!/bin/bash
DATE=`date  +%m-%d-%y`
ITERATION=1
while [ -f ~/HgammaAN/drafts/AN_draft_${DATE}_v${ITERATION}.pdf ];
  do ITERATION=$(($ITERATION + 1))
done
scp johakala@lxplus.cern.ch:/afs/cern.ch/work/j/johakala/private/HgammaSVN/notes/tmp/AN-16-125_temp.pdf ~/HgammaAN/drafts/AN_draft_${DATE}_v${ITERATION}.pdf
