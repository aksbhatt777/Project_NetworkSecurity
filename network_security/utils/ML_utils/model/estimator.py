#Making of a Wrapper class that combines both preprocessor and model into a single pipeline 
# For working on new unseen data in production

from network_security.constants import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os 
import sys 

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    #Wrapper combine preprocessor and model 
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    