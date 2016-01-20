#!/bin/bash
echo $'\n\n---------------------------------------\n\t'$(date)$'\n\n'>> ~/Documents/notesArchive/memos.tx
vim -c 'startinsert' +  ~/Documents/notesArchive/memos.tx
