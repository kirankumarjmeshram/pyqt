from pymongo import MongoClient
import time
import redis
from datetime import datetime

# MongoDB URI
mongo_uri = "mongodb://localhost:27017/myprocess"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db.get_collection('status')

# Connect to Redis
r = redis.Redis()

# Subscribe to the 'tasks' channel in Redis
p = r.pubsub()
p.subscribe('tasks')

while True:
    # Check the MongoDB collection for any pending processes
    pending_documents = list(collection.find({"process": "pending"}))
    if not pending_documents:
        break

    # Check the Redis subscription for new tasks
    message = p.get_message()
    if message and message['type'] == 'message':
        doc_id = message['data']

        print("run triggered")
        # Simulate a long-running process (sleep for 10 seconds)
        for _ in range(10):
            time.sleep(1)
        
        # Update the MongoDB document with the process status
        collection.update_one({"_id": doc_id}, {"$set": {"process": "success"}})
        print(f"Process {doc_id} completed.")
