#!/usr/bin/env python3
"""Redis work in total"""
import redis
import uuid


class Cache():
    """Cache class"""
    def __init__(self):
        """Initialization"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: bytes) -> str:
        """Store to redis"""
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id
