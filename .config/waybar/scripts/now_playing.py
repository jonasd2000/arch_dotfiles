#! /usr/bin/python3
import subprocess
import sys
import re

player_priority = ["spotify", "firefox"]

get_players = subprocess.run(["playerctl", "-l"], capture_output=True)
players = [
    {"name": player} for player in
    get_players.stdout.decode().split("\n")[:-1]
]

if not players:  # if there are no players open
    print("")
    sys.exit(1)

for player in players:
    get_status = subprocess.run(
            ["playerctl", "status",
             "--player", player["name"]],
            capture_output=True
    )
    player["status"] = get_status.stdout.decode().strip()
    player["priority"] = [
        i for i, item in enumerate(player_priority)
        if re.search(item, player["name"])
    ] or [100]

active_players = list(filter(lambda pl: pl["status"] == "Playing", players))

if not active_players:  # if no player is currently playing anything
    print("")
    sys.exit(1)


active_players_prio = sorted(active_players, key=lambda pl: pl["priority"][0])
subprocess.run([
    "playerctl", "metadata",
    "--player", active_players_prio[0]["name"],
    "--format", "{{artist}} - {{title}}"
])
