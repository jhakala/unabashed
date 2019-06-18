random instructions
===================

pyrootOpener
------------

run Automator

File->New

choose Application

scroll down and select Run AppleScript

right click in the area and paste the source code into the box

File->Export

Export As: pyrootOpener.app

Where: Applications

Save

go in Finder and find some ROOT file, right click and do Open With->Other

select pyrootOpener.app and check "Always Open With" box

you should get a prompt saying "pyrootOpener wants to do something or another with iTerm", say yes

it should work -- your file should open in PyROOT in a new iTerm tab and then pop up a TBrowser

it should do this every time you double-click a ROOT file in Finder 
