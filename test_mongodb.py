
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


# uri = MONGO_DB_URL

# Create a new client and connect to the server
client = MongoClient(MONGO_DB_URL)

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

from pymongo import MongoClient

# MONGO_DB_URL = "your_mongo_connection_url"
# client = MongoClient(MONGO_DB_URL)

database_name = "ATHARVJ"
collection_name = "NetworkData"

db = client[database_name]
collection = db[collection_name]

print("Number of records in MongoDB:", collection.count_documents({}))
data = list(collection.find())
print(f"Raw data from MongoDB: {data[:5]}")
import pandas as pd
df = pd.DataFrame(data)
print(f"DataFrame shape after fetching: {df.shape}")
if "_id" in df.columns:
    df.drop(columns=["_id"], inplace=True)
print(df.head())