#!/bin/bash
cd ~/work/public/BHAnalysisNote
svn update utils
svn update -N notes
svn update -N papers
svn update notes/EXO-15-007
svn update notes/AN-15-130
svn update notes/DN-14-042
eval `notes/tdr runtime -sh` 
alias PASmakeDraft="source ~/PASmakeDraft.sh"
alias ANmakeDraft="source ~/ANmakeDraft.sh"
alias DNmakeDraft="rm -f ~/.tmpDN/*; source ~/DNmakeDraft.sh; cp /afs/cern.ch/work/j/johakala/public/BHAnalysisNote/notes/tmp/DN-14-042_temp.pdf ~/.tmpDN"
alias BHmakeDrafts="rm -f ~/.tmpANandPAS/*; PASmakeDraft; cp /afs/cern.ch/work/j/johakala/public/BHAnalysisNote/notes/tmp/EXO-15-007_temp.pdf ~/.tmpANandPAS; ANmakeDraft; cp /afs/cern.ch/work/j/johakala/public/BHAnalysisNote/notes/tmp/AN-15-130_temp.pdf ~/.tmpANandPAS"
cd notes
