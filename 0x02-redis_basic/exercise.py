#!/usr/bin/env python3
"""Redis work in total"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """function counts number of calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of input and output"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wraps decorated function"""
        _input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", _input)
        _output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(_output))
        return _output
    return wrapper


def replay(method: Callable):
    """replay function to display the history
    of calls of a particular function"""
    key = method.__qualname__
    _redis = redis.Redis()

    print('{} was called {:d} times:'.format(key, int(_redis.get(key))))
    inputs = _redis.lrange("{}:inputs".format(key), 0, -1)
    outputs = _redis.lrange("{}:outputs".format(key), 0, -1)

    for inp, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key,
              inp.decode('utf-8'), out.decode('utf-8')))


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialization"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store to redis"""
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get method returns desired format"""
        value = self._redis.get(key)
        if fn:
            fn(value)
        return value

    def get_str(self, key: str) -> str:
        """get from cache as string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """parametrize Cache.get with correct conversion function"""
        return self.get(key, int)
