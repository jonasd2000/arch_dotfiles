#! /usr/bin/python3

import subprocess

from common import get_parser, dispatch

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


def main():
    parser = get_parser()
    args = parser.parse_args()
    dispatch(print_updates, interval=args.interval)


if __name__ == "__main__":
    main()
