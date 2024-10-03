import time
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--interval", type=float,
                        help="the interval between updates of the script")


def dispatch(fn, interval, *args, **kwargs):
    while True:
        t = time.time()
        args, kwargs = fn(*args, **kwargs)
        sleep_time = max(0, interval - (time.time() - t))
        time.sleep(sleep_time)
