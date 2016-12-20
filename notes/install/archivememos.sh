#!/bin/bash
echo "Backing up memos."
memosname=$(echo -n memos_;date "+%F";echo .tx)
newmemos=$(echo $memosname | tr -d ' ')
if [ -f ~/Documents/notes/notesArchive/$newmemos ]; then
  memosname=$(echo -n memos_;date "+%m-%d-%Y_%R:%S";echo .tx)
  newmemos=$(echo $memosname | tr -d ' ')
fi
echo memos.tx is being moved to notesArchive/$newmemos
cp ~/Documents/notes/notesArchive/memos.tx ~/Documents/notes/notesArchive/$newmemos
