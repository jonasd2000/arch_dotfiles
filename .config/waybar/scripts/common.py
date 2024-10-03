import time
import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--interval", type=float,
                        help="the interval between updates of the script")
    return parser


def dispatch(fn, interval, *args, **kwargs) -> None:
    while True:
        t = time.time()
        args, kwargs = fn(*args, **kwargs)
        sleep_time = max(0, interval - (time.time() - t))
        time.sleep(sleep_time)


def _main(fn, *args, **kwargs):
    parser = get_parser()
    cl_args = parser.parse_args()
    dispatch(fn, cl_args.interval, *args, **kwargs)
