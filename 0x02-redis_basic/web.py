#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests
from typing import Callable
from functools import wraps
_redis = __import__('redis').Redis()


def count(fn: Callable) -> Callable:
    """Counts number of url calls"""
    @wraps(fn)
    def wrapper(url):
        _redis.incr(f"count:{url}")
        res = _redis.get(f"cached:{url}")
        if res:
            return res.decode('utf-8')
        res_val = fn(url)
        _redis.set(f"count:{url}", 0)
        _redis.setex(f"cached:{url}", 10, res_val)
        return res_val
    return wrapper


@count
def get_page(url: str) -> str:
    """Get page on url"""
    res = requests.get(url)
    return res.text
