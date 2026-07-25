from dataclasses import dataclass

@dataclass #decorator tell to create a class that stores data mainly 
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
## by storing this data it can be sent directly to next phase as a whole packetc

## above can also be written as 
# class DataIngestionArtifact:
#     def __init__(self, trained_file_path: str, test_file_path: str):
#         self.trained_file_path = trained_file_path
#         self.test_file_path = test_file_path

