from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging  
from network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig

# artifacts are not needed here 
# from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
#for validation 
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation

import sys

if __name__=='__main__':
    try:
        ## For Ingestion 
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(data_ingestion_artifact)

        # For validation 
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_val()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)

        # For Transformation
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        logging.info("Initiated Data transformation")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.start_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation Finished!")

                
    except Exception as e:
        raise NetworkSecurityException(e,sys)