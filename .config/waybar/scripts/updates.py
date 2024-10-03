#! /usr/bin/python3

import subprocess
import json

from common import _main


def get_updates():
    buff_updates = subprocess.run(
        ["checkupdates", "&&", "yay", "-Qua"],
        capture_output=True,
    )
    updates = buff_updates.stdout.decode().split("\n")[:-1]
    return updates


def get_text(updates):
    if len(updates) > 0:
        return ""
    return ""

def get_css_class(updates):
    if len(updates) > 0:
        return "pending"
    return ""


def print_updates():
    updates = get_updates()
    output = {
        "text": get_text(updates),
        "alt": "",
        "tooltip": f"{len(updates)} updates available",
        "class": get_css_class(updates),
        "percentage": "",
    }
    print(json.dumps(output), flush=True)

    return [], {}


if __name__ == "__main__":
    _main(print_updates)
