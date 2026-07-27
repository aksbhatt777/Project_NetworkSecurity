import os
import sys
from datetime import datetime
from network_security import constants 

# check for if entity file is working 
print(constants.PIPELINE_NAME)
print(constants.FILE_NAME)
print(constants.ARTIFACT_DIR)

class TrainingPipelineConfig: ##config used by entire pipeline and other classes 
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=constants.PIPELINE_NAME 
        self.artifact_name=constants.ARTIFACT_DIR #should print "artifacts" 
        self.artifact_dir=os.path.join(self.artifact_name,timestamp) #concat timestamp as a sub dir to artifact
        self.model_dir=os.path.join("final_model") 
        self.timestamp: str=timestamp

## this class initializes the shared configuration that every stage of the MLOps pipeline uses.

class DataIngestionConfig:
    def __init__(self,training_pc:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pc.artifact_dir,constants.DATA_INGESTION_DIR_NAME
        )#create folder path where all data ingestion outputs will be stored
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,constants.DATA_INGESTION_FEATURE_STORE_DIR,constants.FILE_NAME
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,constants.DATA_INGESTION_DIR_NAME,constants.TRAIN_FILE_NAME
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,constants.DATA_INGESTION_DIR_NAME,constants.TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = constants.DATA_INGESTION_TTS_RATIO
        self.collection_name: str = constants.DATA_INGESTION_COLLECTION_NAME 
        self.database_name: str = constants.DATA_INGESTION_DATABASE_NAME

# ============================================================================
# DataIngestionConfig Output (Example)
# ---------------------------------------------------------------------------
# self.data_ingestion_dir -> Artifacts/07_24_2026_11_50_30/data_ingestion
# self.feature_store_file_path -> Artifacts/07_24_2026_11_50_30/data_ingestion/feature_store/phisingData.csv
# self.training_file_path -> Artifacts/07_24_2026_11_50_30/data_ingestion/ingested/train.csv
# self.testing_file_path -> Artifacts/07_24_2026_11_50_30/data_ingestion/ingested/test.csv
# self.train_test_split_ratio -> 0.2
# self.collection_name -> "NetworkData"
# self.database_name -> "akshatAI"
# Artifacts/
# └── 07_24_2026_11_50_30<random_DTstamp>/
#     └── data_ingestion/
#         ├── feature_store/
#         │   └── phisingData.csv
#         └── ingested/
#             ├── train.csv
#             └── test.csv
# ============================================================================


class DataValidationConfig:
    def __init__(self,training_pc:TrainingPipelineConfig):
        self.data_val_dir: str = os.path.join(training_pc.artifact_dir,constants.DATA_VALIDATION_DIR_NAME)
        #print(self.data_val_dir)
        self.valid_data_dir: str = os.path.join(self.data_val_dir, constants.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_val_dir, constants.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, constants.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, constants.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, constants.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, constants.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_val_dir,
            constants.DATA_VALIDATION_DRIFT_REPORT_DIR,
            constants.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
    def __init__(self,training_pc:TrainingPipelineConfig):
        self.data_trans_dir: str = os.path.join(training_pc.artifact_dir,constants.DATA_TRANSFORMATION_DIR_NAME)
        self.trans_train_file_path: str = os.path.join(self.data_trans_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,constants.TRAIN_FILE_NAME.replace("csv","npy"))
        self.trans_test_file_path: str = os.path.join(self.data_trans_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,constants.TEST_FILE_NAME.replace("csv","npy"))
        self.trans_obj_file_path: str = os.path.join(self.data_trans_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,constants.PREPROCESSING_OBJECT_FILE_NAME) 
    ## └── data_transformation/
                    # ├── transformed/
                    # │   ├── train.npy
                    # │   └── test.npy
                    # └── transformed_object/
                    #     └── preprocessing.pkl



            
