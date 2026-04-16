from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["b2b_database"]

collection = db["startups"]

collection.create_index(
    "name",
    unique=True
)


def save_to_database(data):

    if not data:
        print("No data to insert")
        return

    try:

        result = collection.insert_many(
            data,
            ordered=False
        )

        print(
            "Inserted records:",
            len(result.inserted_ids)
        )

    except BulkWriteError as e:

        duplicates = len(
            e.details["writeErrors"]
        )

        print(
            "Duplicates skipped:",
            duplicates
        )