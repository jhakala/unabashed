#!/bin/bash
echo $'\n\n---------------------------------------\n\t'$(date)$'\n\n'>> ~/Documents/notesArchive/notes.tx
vim -c 'startinsert' +  ~/Documents/notesArchive/notes.tx
