#!/bin/bash
~/Documents/archivenotes.sh
echo "       --------------" > ~/Documents/notesArchive/notes.tx
echo "      | John's Notes |" >> ~/Documents/notesArchive/notes.tx
echo "       --------------" >> ~/Documents/notesArchive/notes.tx
echo >> ~/Documents/notesArchive/notes.tx
echo -n "  continued from " >> ~/Documents/notesArchive/notes.tx
ls -rt ~/Documents/notesArchive | grep notes_ | tail  -1 >> ~/Documents/notesArchive/notes.tx
~/Documents/notes.sh
