#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests
from typing import Callable
from functools import wraps
_redis = __import__('redis').Redis()


def count(fn: Callable) -> None:
    """Counts number of url calls"""
    @wraps(fn)
    def wrapper(url):
        _redis.incr(f"count:{url}")
        res = _redis.get(f"cached:{url}")
        if res:
            return res.decode('utf-8')
        res = fn(url)
        _redis.setex(f"cached:{url}", 10, res)
        return res
    return wrapper


@count
def get_page(url: str) -> str:
    """Get page on url"""
    res = requests.get(url)
    return res.text
