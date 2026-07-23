import os
import json 
import sys

## load env variable 
from dotenv import load_dotenv
load_dotenv()

## mongodb credentials 
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi 
ca=certifi.where()


import pandas as pd 
import numpy as np 
import pymongo 
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


class ETL():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)  # acc to it first param is error msg and second is sys


    def csv_to_json(self,file_path): ## data transformation 
        try:
            ## refer the ipynb for logic 
            df=pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records=list(json.loads(df.T.to_json()).values()) #transposed, to json, convert proper json dict format , took out the values 
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) ## creating a connection with mongo db server, communicate with cluster 
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]

            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    


if __name__=='__main__':
    FILE_PATH="data/phisingData.csv"
    DATABASE="AkshatAI"
    Collection="NetworkData"
    networkobj=ETL() ## onject instantiation
    records=networkobj.csv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_to_mongodb(records,DATABASE,Collection)
    print(no_of_records)    


