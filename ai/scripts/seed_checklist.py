import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.smoothmigration
collection = db.checklist


sample_tasks = [
    {
        "category": "Pre-Departure",
        "description": "Apply for visa",
        "completed": False
    },
    {
        "category": "Pre-Departure",
        "description": "Find temporary housing",
        "completed": False
    },
    {
        "category": "Post-Arrival",
        "description": "Register with local authority",
        "completed": False
    }
]


result = collection.insert_many(sample_tasks)
print(f"Inserted {len(result.inserted_ids)} tasks into MongoDB.")
