#!/bin/bash
tmux new-session -s matrix -n myWindow -d 'I=1; while :; do sed "$I{q};d" /tmp/ccm_all.dump; I=$(($I+1)); sleep .025; done'\;        split-window -h -d 'I=5000; while :; do sed "$I{q};d" /tmp/ccm_all.dump; I=$(($I+1)); sleep .045; done'\; split-window -h -d 'I=15000; while :; do sed "$I{q};d" /tmp/ccm_all.dump; I=$(($I+1)); sleep .035; done'\; attach-session
