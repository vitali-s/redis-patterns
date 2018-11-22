import pipes
import time
from connection import connection

PRECISION = [1, 60, 300, 3600, 18000]
COUNTER_KEY = 'hits'


def save_counter(count):
    # get current time
    now = time.time()
    pipe = connection.pipeline()

    for precision in PRECISION:
        pnow = int(now / precision) * precision

        # increment counter
        pipe.hincrby(get_count_hash_key(precision), pnow, count)

    pipe.execute()


def get_counter(precision):
    counters = connection.hgetall(get_count_hash_key(precision))

    # transform to int
    result = counters.map(lambda key, value: int(key), int(value))

    result.sort()
    return result


def get_known_hash_key(precision):
    return f'known:{precision}:{COUNTER_KEY}'


def get_count_hash_key(precision):
    return f'count:{precision}:{COUNTER_KEY}'
