#!/bin/bash
# Script to install John's notes scripts
# John Hakala, 4/20/2016
set -e

if [ -d ~/Documents/notes ]; then
  echo "Documents/notes was found! Will not make a new one."
else
  mkdir ~/Documents/notes
fi

cp ~/unabashed/notes/install/* ~/Documents/notes

if [ -d ~/Documents/notes/notesArchive ]; then
  echo "Documents/notes/notesArchive was found! Will not make a new one."
else
  mkdir ~/Documents/notes/notesArchive
fi

if [ -f ~/Documents/notes/notesArchive/notes.tx ]; then
  echo "Documents/notes/notesArchive/notes.tx was found! notes installation aborted!!"
  exit 1
fi

read -p "Press any key to continue."
~/Documents/notes/freshnotes.sh freshinstall
~/Documents/notes/freshmemos.sh freshinstall
