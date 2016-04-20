#!/bin/bash
echo $'\n\n---------------------------------------\n\t'$(date)$'\n\n'>> ~/Documents/notes/notesArchive/memos.tx
vim -c 'startinsert' +  ~/Documents/notes/notesArchive/memos.tx
