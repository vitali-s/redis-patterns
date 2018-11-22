import redis
import time
import json

LAST_CHECKED = None
IS_UNDER_MAINTENANCE = False
KEY_IS_UNDER_MAINTENANCE = 'is-under-maintenance'

connection = redis.Redis(host='127.0.0.1', port=6379, db=0)

def is_under_maintenance():
    global LAST_CHECKED, IS_UNDER_MAINTENANCE

    if LAST_CHECKED < time.time():
        LAST_CHECKED = time.time()

        IS_UNDER_MAINTENANCE = bool(connection.get(KEY_IS_UNDER_MAINTENANCE))

    return IS_UNDER_MAINTENANCE

def set_config(type, component, config):
    key = f'config:{type}:{component}'

    connection.set(key, json.dump(config))

CONFIGS = {}
CHECKED = {}

def get_config(type, component, wait = 1)
    key = f'config:{type}:{component}'
    
    if CHECKED.get(key) < time.time() - wait:
        CHECKED[key] = time.time()

        config = json.loads(connection.get(key) or '{}')
        config = dict((str(k), config[k]) for k in config)

        old_config = CONFIGS.get(key)

        if config != old_config:
            CONFIGS[key] = config

    return CONFIGS.get(key)
