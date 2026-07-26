from network_security.entity.config_entity import DataValidationConfig
from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.constants import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp # for data drift check 
import pandas as pd
import os,sys
from network_security.utils.main_utils.utils import read_yaml,write_yaml


class DataValidation:
    def __init__(self,dia:DataIngestionArtifact,dvc:DataValidationConfig):
        """ input is data ingestion artifact , output is data validation config"""
        try:
            self.dia=dia #input
            self.dvc=dvc #output
            self._schema_config = read_yaml(SCHEMA_FILE_PATH) #proctected attribute -- encapsulation
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_cols(self,df:pd.DataFrame) -> bool: #as while comparing with yaml schema we get a bool o/p
        try:
            num_of_cols=len(self._schema_config) #from schema file used for comparison 
            logging.info(f"Required number of columns:{num_of_cols}")
            logging.info(f"Data frame has columns:{len(df.columns)}") # from the df picked from artifact 
            if len(df.columns)==num_of_cols: ## if statemnt can show clear intent of the code 
                return True
            else:
                return False
            #return len(df.columns) == num_of_cols # returns True is same , False if not .. does the same as above

        except Exception as e:
            raise NetworkSecurityException(e,sys)  


    def detect_data_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                pval_found=is_same_dist.pvalue
                if pval_found >= threshold:
                    is_found=False #no drift 
                else:
                    is_found=True #drift detected (pval < 0.05) 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found                  
                    }})
            drift_report_file_path = self.dvc.drift_report_file_path 
            #create dir 
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml(file_path=drift_report_file_path,content=report)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_val(self) -> DataValidationArtifact:
        try:
            #input is taken from data ingestion artifact
            train_file_path=self.dia.trained_file_path 
            test_file_path=self.dia.test_file_path

            #read data from artifact -> using the static method
            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path)    

            #validate cols 
            status=self.validate_cols(df=train_df) #this o/p is a bool
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status=self.validate_cols(df=test_df) #this o/p is a bool
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"

            #check data drift -- again o/p is bool
            drift_status=self.detect_data_drift(base_df=train_df,current_df=test_df)

            #make dir for validated df to save them 
            dir_path=os.path.dirname(self.dvc.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(self.dvc.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.dvc.valid_test_file_path, index=False, header=True)

            ## put all in artifact 
            # data is saved regardless - valid or invalid in same location - status tells story
            data_val_artifact=DataValidationArtifact(
                validation_status=status, #status for columns 
                valid_train_file_path=train_file_path,
                valid_test_file_path=test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_status=drift_status,
                drift_report_file_path=self.dvc.drift_report_file_path
            )
            return data_val_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
