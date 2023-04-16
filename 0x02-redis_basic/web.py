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
        return fn(url)
    return wrapper


@count
def get_page(url: str) -> str:
    """Get page on url"""
    res = _redis.get(url)
    if (res is not None):
        return res.decode('utf-8')
    res = requests.get(url)
    _redis.set(url, res.text)
    _redis.expire(url, 10)
    return res
