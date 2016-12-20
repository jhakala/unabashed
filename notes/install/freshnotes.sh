#!/bin/bash
set -e
if [ "$1" = "freshinstall" ]; then
  if [ -f ~/Documents/notes/notesArchive/notes.tx ]; then
    echo "freshinstall was called for freshnotes.sh, but it seems there are already notes in Documents/notes/notesArchive!"
    exit 1
  else
    echo " Doing a fresh install of notes."
    echo "       --------------" > ~/Documents/notes/notesArchive/notes.tx
    echo "      | John's Notes |" >> ~/Documents/notes/notesArchive/notes.tx
    echo "       --------------" >> ~/Documents/notes/notesArchive/notes.tx
    echo >> ~/Documents/notes/notesArchive/notes.tx
    DATE=`date`
    echo -n "  Welcome to John's notes." >> ~/Documents/notes/notesArchive/notes.tx
    echo -n " Installed on ${DATE}  " >> ~/Documents/notes/notesArchive/notes.tx
    ~/Documents/notes/notes.sh
  fi
else
  echo " Making some fresh notes."
  ~/Documents/notes/archivenotes.sh
  echo "       --------------" > ~/Documents/notes/notesArchive/notes.tx
  echo "      | John's Notes |" >> ~/Documents/notes/notesArchive/notes.tx
  echo "       --------------" >> ~/Documents/notes/notesArchive/notes.tx
  echo >> ~/Documents/notes/notesArchive/notes.tx
  echo -n "  continued from " >> ~/Documents/notes/notesArchive/notes.tx
  ls -rt ~/Documents/notes/notesArchive | grep notes_ | tail  -1 >> ~/Documents/notes/notesArchive/notes.tx
  ~/Documents/notes/notes.sh
fi
