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
        """warap the decorated function"""
        self._redis.incr(key)
        return method
    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Initialization"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

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
