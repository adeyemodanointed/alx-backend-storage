#!/usr/bin/env python3
"""Log stats - new version"""
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
    ips = nginx_collection.aggregate([
                {
                    "$group": {
                        "_id": "$ip",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {
                        "count": -1
                    }
                },
                {"$limit": 10}
        ])
    print('IPs:')
    for ip in ips:
        print('{}{}: {}'.format('\t', ip.get('_id'), ip.get('count')))


if __name__ == "__main__":
    log_stats()
