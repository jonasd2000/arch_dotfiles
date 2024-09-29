#!/usr/bin/bash

status_paused="Paused"
status_no_players="No players found"
status_playing="Playing"

current_status="$(playerctl status 2>&1)"

if [[ "$current_status" == "$status_paused" ]]; then
    echo ""
    exit 1
elif [[ "$current_status" == "$status_no_players" ]]; then
    echo ""
    exit 1
elif [[ "$current_status" == "$status_playing" ]]; then
    echo "$(playerctl metadata artist) - $(playerctl metadata title)"
fi
