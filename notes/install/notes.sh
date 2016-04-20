#!/bin/bash
echo $'\n\n---------------------------------------\n\t'$(date)$'\n\n'>> ~/Documents/notes/notesArchive/notes.tx
vim -c 'startinsert' +  ~/Documents/notes/notesArchive/notes.tx
