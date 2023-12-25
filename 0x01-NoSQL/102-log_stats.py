#!/usr/bin/env python3

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.logs
collection = db.nginx

total_documents = collection.count_documents({})

print(f"{total_documents} logs\nMethods:")

# Display methods count
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\tmethod {method}: {count} logs")

# Display count for method=GET an
status_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_count} status check")

top_ips = collection.aggregate([
    {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])

print("IPs:")
for ip_info in top_ips:
    print(f"\t{ip_info['_id']}: {ip_info['count']}")

client.close()
