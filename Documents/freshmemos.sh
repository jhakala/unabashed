#!/bin/bash
~/Documents/archivememos.sh
echo "       --------------" > ~/Documents/notesArchive/memos.tx
echo "      | John's Memos |" >> ~/Documents/notesArchive/memos.tx
echo "       --------------" >> ~/Documents/notesArchive/memos.tx
echo >> ~/Documents/notesArchive/memos.tx
echo -n "  continued from " >> ~/Documents/notesArchive/memos.tx
ls -rt ~/Documents/notesArchive | grep memos_ | tail  -1 >> ~/Documents/notesArchive/memos.tx
~/Documents/memos.sh
