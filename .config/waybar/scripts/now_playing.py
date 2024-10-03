#! /usr/bin/python3
import subprocess
import re

from common import get_parser, dispatch


MAX_OUTPUT_LENGTH = 30


class NowPlaying:
    def __init__(self, player_priority) -> None:
        self.status = ""
        self.players = []
        self.active_players = []

        self.player_priority = player_priority

    def get_players(self):
        output_players = subprocess.run(
            ["playerctl", "-l"],
            capture_output=True
        )
        players = [
            {"name": player} for player in
            output_players.stdout.decode().split("\n")[:-1]
        ]

        if not players:  # if there are no players open
            return

        for player in players:
            output_status = subprocess.run(
                    ["playerctl", "status",
                     "--player", player["name"]],
                    capture_output=True
            )
            player["status"] = output_status.stdout.decode().strip()
            player["priority"] = [
                i for i, item in enumerate(self.player_priority)
                if re.search(item, player["name"])
            ] or [100]

        return players

    def get_active_players(self):
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

    def get_status(self) -> str:
        if not self.players:
            return ""
        if not self.active_players:
            return ""
        return self.get_playing_output()

    def update(self) -> None:
        self.players = self.get_players()
        self.active_players = self.get_active_players()
        self.status = self.get_status()


def scroll_text(text: str, max_characters: int, offset: int):
    if len(text) < max_characters:
        return text
    text += ". "
    overhang = (offset + max_characters) - len(text)
    post = ""
    if overhang > 0:
        post = text[:overhang]

    return text[offset:offset+max_characters] + post


def print_status(now_playing: NowPlaying, old_status: str = "", i: int = 0):
    now_playing.update()

    if now_playing.status != old_status:
        i = 0
    text_offset = i % len(now_playing.status)

    print(
        scroll_text(
            now_playing.status,
            max_characters=MAX_OUTPUT_LENGTH,
            offset=text_offset
        ),
        flush=True
    )

    i += 1
    old_status = now_playing.status

    return [], {"now_playing": now_playing, "old_status": old_status, "i": i}


def main():
    parser = get_parser()
    parser.add_argument("-P", "--player-priority", nargs="*", default=[])
    args = parser.parse_args()

    now_playing = NowPlaying(player_priority=args.player_priority)

    dispatch(
        fn=print_status,
        interval=args.interval,
        now_playing=now_playing,
    )


if __name__ == "__main__":
    main()
