import os
import sys
import numpy as np
import pandas as pd
import pymongo

from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact ## this is for storing the output

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def read_from_mongodb(self):
        """export collection as a df from mongodb"""
        try:
            db_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) #self makes it for other method to access it to later if needed
            collection=self.mongo_client[db_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True) # no need but just for sake 
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def export_to_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path # this stores the string
            dir_path=os.path.dirname(feature_store_file_path) # extract dir name from path string
            os.makedirs(dir_path,exist_ok=True) #made a dir named featurestore like this 

            df.to_csv(feature_store_file_path,index=False,header=True)
            return df 
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def tts(self,df:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path=os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_path,exist_ok=True) #both train and test.csv will be in same dir

            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False)
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        "This method uses all the methods made in this class"
        try:
            df=self.read_from_mongodb() # df is taken from mongodb
            df=self.export_to_feature_store(df) # raw df is exported to feature store 
            self.tts(df) # not saved to a variable as no return is here 
            # first create a Data Ingestion Artifact class 
            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact ## now when running this we assign it to a variable
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
