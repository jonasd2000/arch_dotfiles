import time


def dispatch(fn, interval, *args, **kwargs):
    while True:
        t = time.time()
        args, kwargs = fn(*args, **kwargs)
        sleep_time = max(0, interval - (time.time() - t))
        time.sleep(sleep_time)
