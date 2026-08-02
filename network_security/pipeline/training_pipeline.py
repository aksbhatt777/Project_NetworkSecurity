## exactly as main.py .. but in a class format 

import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

# import components
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

# import entities config
from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

# import artifacts 
from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from network_security.constants import SAVED_MODEL_DIR


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion():
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_validation():
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_transformation():
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_trainer():
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    