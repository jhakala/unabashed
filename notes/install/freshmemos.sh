#!/bin/bash
set -e
if [ "$1" = "freshinstall" ]; then
  if [ -f ~/Documents/notes/notesArchive/memos.tx ]; then
    echo "freshinstall was called for freshmemos.sh, but it seems there are already memos in Documents/notes/notesArchive!"
    exit 1
  else
    echo "       --------------" > ~/Documents/notes/notesArchive/memos.tx
    echo "      | John's Memos |" >> ~/Documents/notes/notesArchive/memos.tx
    echo "       --------------" >> ~/Documents/notes/notesArchive/memos.tx
    echo >> ~/Documents/notes/notesArchive/memos.tx
    DATE=`date`
    echo -n "  Welcome to John's memos." >> ~/Documents/notes/notesArchive/memos.tx
    echo -n " Installed on ${DATE}  " >> ~/Documents/notes/notesArchive/memos.tx
    ~/Documents/notes/memos.sh
  fi
else
  echo " Making some fresh memos."
  ~/Documents/notes/archivememos.sh
  echo "       --------------" > ~/Documents/notes/notesArchive/memos.tx
  echo "      | John's Memos |" >> ~/Documents/notes/notesArchive/memos.tx
  echo "       --------------" >> ~/Documents/notes/notesArchive/memos.tx
  echo >> ~/Documents/notes/notesArchive/memos.tx
  echo -n "  continued from " >> ~/Documents/notes/notesArchive/memos.tx
  ls -rt ~/Documents/notes/notesArchive | grep memos_ | tail  -1 >> ~/Documents/notes/notesArchive/memos.tx
  ~/Documents/notes/memos.sh
fi
