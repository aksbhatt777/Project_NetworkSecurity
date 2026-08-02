from dataclasses import dataclass

@dataclass #decorator tell to create a class that stores data mainly 
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
## by storing this data it can be sent directly to next phase as a whole packetc

# # above can also be written as 
# class DataIngestionArtifact:
#     def __init__(self, trained_file_path: str, test_file_path: str):
#         self.trained_file_path = trained_file_path
#         self.test_file_path = test_file_path

@dataclass 
class DataValidationArtifact:
    validation_status: bool
    drift_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass 
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact



