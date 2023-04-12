#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def log_stats():
    """provides some stats about Nginx logs stored in MongoDB"""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    client = MongoClient('mongodb://localhost:27017')
    nginx_collection = client.logs.nginx

    count = nginx_collection.count_documents({})
    print('{} logs'.format(count))
    print('Methods:')
    for method in methods:
        print('{}method {}: {}'.format('\t', method,
              nginx_collection.count_documents({"method": method})))
    print('{} status check'.format(
          nginx_collection.count_documents(
              {"method": "GET", "path": "/status"})))


log_stats()
