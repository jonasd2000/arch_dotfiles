#! /usr/bin/python3

import subprocess

from common import _main

INTERVAL = 5


def get_updates():
    buff_updates = subprocess.run(
        ["checkupdates", "&&", "yay", "-Qua"],
        capture_output=True,
    )
    updates = buff_updates.stdout.decode().split("\n")[:-1]
    return updates


def print_updates():
    updates = get_updates()
    print(len(updates))

    return [], {}


if __name__ == "__main__":
    _main(print_updates)
