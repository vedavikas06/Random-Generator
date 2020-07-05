import redis
import traceback
from flask import abort, request
from functools import wraps
from app import app
from flask_login import login_required, current_user

#Rate Limiter Using redis
r = redis.Redis(decode_responses=True)

print(r.connection_pool)

def rate_limiter(fn=None, limit=5, minutes=1):
    """Limits requests to this endpoint to `limit` per `minutes`."""

    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if limit < 1:
        raise Exception('Limit must be greater than zero.')
    
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            
            if current_user.is_authenticated:
                if get_count(type='user') < limit:
                    increment_counter(type='user', minutes=minutes)
                else:
                    return abort(403,description = "Request Limit Exhausted! Try again later")
            else:
                return abort(403,description = "Please login and Try again!!")
            return func(*args, **kwargs)

        return inner
    return wrapper(fn) if fn else wrapper

def remaining_requests(limit):
    try:
        rem_requests = limit - get_count(type='user')
        return rem_requests
    except:
        app.logger.error("error processing the request")
        abort(404,description = "Error Processing the remaining limits")
        return 0

def get_counter_key(type=None): 
    
    if type == 'user':
        key = current_user.username if current_user.is_authenticated else None
    else:
        raise Exception('Unknown rate limit type: {0}'.format(type))
    
    return ('{type}-{key}').format(
        type=type,
        key=key,
    )

def increment_counter(type=None, minutes=1):
    if type not in ['user']:
        raise Exception('Type must be user.')

    key = get_counter_key(type=type)
    try:
        r.set(key,0,ex=60,nx=True)
        r.incr(key)
        # r.expire(key, time=60 * minutes)
    except:
        app.logger.error(traceback.format_exc())
        pass

def get_count(type=None):
    key = get_counter_key(type=type)
    
    try:
        return int(r.get(key) or 0)
    except:
        app.logger.error(traceback.format_exc())
        return 0