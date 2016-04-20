#!/bin/bash
echo "Backing up notes."
notesname=$(echo -n notes_;date "+%F";echo .tx)
newnotes=$(echo $notesname | tr -d ' ')
if [ -f ~/Documents/notes/notesArchive/$newnotes ]; then
  notesname=$(echo -n notes_;date +"%m-%d-%Y_%R:%S";echo .tx)
  newnotes=$(echo $notesname | tr -d ' ')
fi
echo notes.tx is being moved to notesArchive/$newnotes
cp ~/Documents/notes/notesArchive/notes.tx ~/Documents/notes/notesArchive/$newnotes
