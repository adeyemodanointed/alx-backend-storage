#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
s2 = cache.store("secont")
s3 = cache.store("third")
replay = __import__('exercise').replay

replay(cache.store)
