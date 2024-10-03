#! /usr/bin/python3
import subprocess
import re
import json
from enum import Enum

from common import get_parser, dispatch


MAX_OUTPUT_LENGTH = 30


class NowPlayingStatus(Enum):
    NoPlayers = -1
    Paused = 0
    Playing = 1


class NowPlaying:
    status: NowPlayingStatus

    def __init__(self, player_priority) -> None:
        self.status = NowPlayingStatus.NoPlayers
        self.players = []
        self.active_players = []

        self.player_priority = player_priority

    def get_players(self):
        # get available players
        output_players = subprocess.run(
            ["playerctl", "-l"],
            capture_output=True
        )
        players = [
            {"name": player} for player in
            output_players.stdout.decode().split("\n")[:-1]
        ]

        if not players:  # if there are no players available
            return

        # for each available player
        for player in players:
            # get its status
            output_status = subprocess.run(
                    ["playerctl", "status",
                     "--player", player["name"]],
                    capture_output=True
            )
            player["status"] = output_status.stdout.decode().strip()
            # set its priority according to player_priority
            player["priority"] = [
                i for i, item in enumerate(self.player_priority)
                if re.search(item, player["name"])
            ] or [100]

        return players

    def get_active_players(self):
        if not self.players:
            return

        active_players = list(filter(
            lambda pl: pl["status"] == "Playing",
            self.players
        ))
        return active_players

    def get_playing_output(self) -> str:
        active_players_prio = sorted(
            self.active_players,
            key=lambda pl: pl["priority"][0]
        )
        get_output = subprocess.run([
            "playerctl", "metadata",
            "--player", active_players_prio[0]["name"],
            "--format", "{{artist}} - {{title}}"
        ], capture_output=True)

        return get_output.stdout.decode().strip()

    def get_status(self):
        if self.active_players:
            return NowPlayingStatus.Playing
        if self.players:
            return NowPlayingStatus.Paused

        return NowPlayingStatus.NoPlayers

    def output_text(self) -> str:
        match self.status:
            case NowPlayingStatus.NoPlayers:
                return ""
            case NowPlayingStatus.Paused:
                return ""
            case NowPlayingStatus.Playing:
                return self.get_playing_output()

    def update(self) -> None:
        self.players = self.get_players()
        self.active_players = self.get_active_players()
        self.status = self.get_status()


def scroll_text(text: str, max_characters: int, step: int):
    if len(text) < max_characters:
        return text

    offset = step % len(text)
    text += ". "
    overhang = (offset + max_characters) - len(text)
    post = ""
    if overhang > 0:
        post = text[:overhang]

    return text[offset:offset+max_characters] + post


def get_css_class(now_playing):
    match now_playing.status:
        case NowPlayingStatus.NoPlayers:
            return "noplayers"
        case NowPlayingStatus.Paused:
            return "paused"
        case NowPlayingStatus.Playing:
            return "playing"
        case _:
            return ""


def print_status(now_playing: NowPlaying, old_output: str = "", i: int = 0):
    now_playing.update()
    now_playing_output = now_playing.output_text()

    if now_playing_output != old_output:
        i = 0

    output = {
            "text": scroll_text(
                now_playing_output,
                max_characters=MAX_OUTPUT_LENGTH,
                step=i),
            "alt": "",
            "tooltip": now_playing_output,
            "class": get_css_class(now_playing),
            "percentage": "",
    }

    print(json.dumps(output), flush=True)

    i += 1
    kwargs = {
        "now_playing": now_playing,
        "old_output": now_playing_output,
        "i": i,
    }
    return [], kwargs


def main():
    parser = get_parser()
    parser.add_argument("-P", "--player-priority", nargs="*", default=[])
    args = parser.parse_args()

    now_playing = NowPlaying(player_priority=args.player_priority)
    kwargs = {"now_playing": now_playing}

    dispatch(
        fn=print_status,
        interval=args.interval,
        **kwargs
    )


if __name__ == "__main__":
    main()
