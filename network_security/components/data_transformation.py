import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from network_security.entity.config_entity import DataTransformationConfig
from network_security.logging.logger import logging

from network_security.constants import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.constants import TARGET_COLUMN
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        #dva-i/p and dtc-o/p ... after pipeline ends dtc becomes dta 
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def get_transform_obj(cls) -> Pipeline:
        "only does knn imputation but is scalable for diff scenarios"
        #class method , returns pipeline obj (hint)  
        logging.info("entered get_transform_method of Transformation class")
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            # ** used for loading dict into keyword args
            logging.info(f"Initialised imputer with : {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor=Pipeline([("imputer",imputer)]) #firt arg- name , 2nd actual obj
            #list can take multiple tuples -- which are the mutiple scinarios eg: ("scaler", StandardScaler())
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def start_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered start_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            #Read df from data validation artifact 
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #Training Dataframe
            X_train=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_train=train_df[TARGET_COLUMN]
            y_train=train_df.replace(-1,0)

            #Test DF
            X_test=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            y_test=test_df[TARGET_COLUMN]
            y_test=test_df.replace(-1,0)

            #calling the pipeline processor 
            preprocessor=self.get_transform_obj() #calls instance method
            preprocessor_obj=preprocessor.fit(X_train) #learns from imputer.fit 
            transformed_X_train=preprocessor_obj.transform(X_train) #applies using transform 
            transformed_X_test=preprocessor_obj.transform(X_test)

            #Combining X and y to whole train and test np array
            train_arr=np.c_[transformed_X_train,np.array(y_train)]
            test_arr=np.c_[transformed_X_test,np.array(y_test)]

            #save this concatenated np array
            #param1- filepath/file name as what data is supposed to be saved 
            #param2 - the file obtained in the step above  
            save_numpy_array_data(self.data_transformation_config.trans_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.trans_test_file_path,test_arr)
            save_object(self.data_transformation_config.trans_obj_file_path,preprocessor_obj)

            # Adding push for preprocessing file 
            save_object("final_model/preprocessor.pkl",preprocessor_obj)

            #Preping artifacts 
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.trans_obj_file_path,
                transformed_train_file_path=self.data_transformation_config.trans_train_file_path,
                transformed_test_file_path=self.data_transformation_config.trans_test_file_path
            )
            return data_transformation_artifact             
           

        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
