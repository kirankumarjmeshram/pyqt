from pymongo import MongoClient
import time

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

def long_running_task():
    # Simulate a long-running process (sleep for 10 seconds)
    for _ in range(10):
        time.sleep(1)

def run_worker():
    while True:
        # Check the MongoDB collection for any pending processes
        # Sort by timestamp to ensure FIFO order
        pending_document = collection.find_one({"process": "pending"}, sort=[("timestamp", 1)])
        if pending_document is not None:
            doc_id = pending_document["_id"]
            print("run triggered")
            long_running_task()
            
            # Update the MongoDB document with the process status
            collection.update_one({"_id": doc_id}, {"$set": {"process": "success"}})
            print(f"Process {doc_id} completed.")
