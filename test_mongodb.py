
from pymongo.mongo_client import MongoClient
import os

uri = "mongodb+srv://atharvjadhav2910:Atharv29@cluster0.xipoi4u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)