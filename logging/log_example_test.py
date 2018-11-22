import time
import pipes
import pytest
import uuid
from connection import connection
from log_example import log, LOG_KEY, LOGSTATS_KEY


@pytest.fixture(scope="session")
def before_test():
    # clean-up log before test
    connection.delete(LOG_KEY)


def test_log_should_store_message_in_list():
    message = str(uuid.uuid4())
    log(message)

    actualMessage = connection.lpop(LOG_KEY).decode()
    assert message in actualMessage


def test_log_should_store_message_on_top_of_the_list():
    for i in range(5):
        message = str(uuid.uuid4())
        log(message)

    actualMessage = connection.lpop(LOG_KEY).decode()
    assert message in actualMessage


def test_log_should_store_only_5_latest_messages():
    for i in range(10):
        message = str(uuid.uuid4())
        log(message)

    length = connection.llen(LOG_KEY)
    assert length == 5


def test_log_should_increment_message_statistics():
    count = 5
    message = str(uuid.uuid4())

    for i in range(count):
        log(message)

    actualCount = connection.zscore(LOGSTATS_KEY, message)
    assert actualCount == count
