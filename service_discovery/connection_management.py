import redis

REDIS_CONNECTIONS = {}

def redis_connection(component, wait = 1):
    key = f'config:redis:{component}'

    def wrapper(function):
        @functools.wraps(function)
        def call(*args, **kwargs):
            old_config = CONFIGS.get(key, object())

            _config = get_config(config_connection, 'redis', component, wait)

            config = {}

            for k, v in _config.iteritems():
                config[k.encode('utf-8')] = v

            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)

            return function(REDIS_CONNECTIONS.get(key), *args, **kwargs)

        return call
    
    return wrapper

@redis_connection('logs')
def log_recent(connection, app, message):
    'function code'

log_recent('app', 'message')