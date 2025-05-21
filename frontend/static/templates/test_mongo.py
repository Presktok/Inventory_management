from pymongo import MongoClient
from datetime import datetime

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.supply_chain_db
    test_collection = db.test
    test_doc = {"name": "standalone_test", "timestamp": datetime.utcnow()}
    test_collection.insert_one(test_doc)
    documents = list(test_collection.find({}, {'_id': 0}))
    print("MongoDB connection successful!")
    print("Test documents:", documents)
except Exception as e:
    print(f"MongoDB connection failed: {e}")