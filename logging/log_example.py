import time
import pipes
from connection import connection

LOG_KEY = 'log'
LOGSTATS_KEY = 'log:states'

def log(message):
    messageWithTime = time.asctime() + ': ' + message

    pipe = connection.pipeline()

    # push message to the top
    pipe.lpush(LOG_KEY, messageWithTime)

    # trip log
    pipe.ltrim(LOG_KEY, 0, 4)
    pipe.zincrby(LOGSTATS_KEY, 1, message)
    pipe.execute()
