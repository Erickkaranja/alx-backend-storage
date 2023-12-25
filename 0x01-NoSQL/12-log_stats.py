#!/usr/bin/env python3
"""module that counts the number of methods called in a bson file."""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_documents = collection.count_documents({})
    print(f"{total_documents} logs/nMethods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = collection.count_documents({"methods": method})
        print(f"    method {method}: {count}")

    status_count = collection.count_documents({"method": "GET",
                                              "path": "/status"})
    print(f"{status_count} status check")

    client.close()
