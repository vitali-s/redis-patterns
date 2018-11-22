import time
import pipes
import pytest
import uuid
import random
from connection import connection
from counters_example import save_counter, get_count_hash_key, PRECISION

def test_get_counters():
    # clean-up counters
    for precision in PRECISION:
        connection.delete(get_count_hash_key(precision))

    # generate 100 random counters
    for i in range(100):
        counter = random.randint(0, 1000)
        save_counter(counter)

    counters = connection.hkeys(get_count_hash_key(PRECISION[1]))

    assert len(counters) == 1

    # assert actualCounter == None
