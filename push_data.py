import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
#print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
        
"""
records : 
[
{"a":1,"b":4,"c":8},
{"a":3,"b":5,"c":2},
{"a":10,"b":44,"c":81},
...
]

"""
if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "ATHARVJ"
    Collection = "NetworkData"
    network_obj = NetworkDataExtract()
    RECORDS = network_obj.csv_to_json(FILE_PATH)
    print(RECORDS)
    no_of_records = network_obj.insert_data_to_mongodb(records=RECORDS,database=DATABASE,collection=Collection)
    print(no_of_records)