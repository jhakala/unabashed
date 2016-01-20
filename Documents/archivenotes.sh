#!/bin/bash
echo "Backing up notes."
notesname=$(echo -n notes_;date "+%F";echo .tx)
newnotes=$(echo $notesname | tr -d ' ')
if [ -f ~/Documents/notesArchive/$newnotes ]; then
  notesname=$(echo -n notes_;date +"%m-%d-%Y_%R:%S";echo .tx)
  newnotes=$(echo $notesname | tr -d ' ')
fi
echo notes.tx is being moved to notesArchive/$newnotes
cp ~/Documents/notesArchive/notes.tx ~/Documents/notesArchive/$newnotes
