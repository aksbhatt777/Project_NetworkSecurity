#Making of a Wrapper class that combines both preprocessor and model into a single pipeline 
# For working on new unseen data in production

from network_security.constants import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os 
import sys 

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

# class NetworkModel:
#     def __init__(self,preprocessor,model):
#         try:
#             self.preprocessor=preprocessor
#             self.model=model
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)

#     #Wrapper combine preprocessor and model 
#     def predict(self,x):
#         try:
#             x_transform=self.preprocessor.transform(x)
#             y_hat=self.model.predict(x_transform)
#             return y_hat
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def _clean_data(self, X):
        """Clean and prepare input data for prediction"""
        try:
            # If X is a DataFrame, clean it
            if hasattr(X, 'columns'):
                X_clean = X.copy()
                
                # Get expected columns from preprocessor
                if hasattr(self.preprocessor, 'feature_names_in_'):
                    expected_cols = list(self.preprocessor.feature_names_in_)
                    
                    # Ensure all expected columns are present
                    for col in expected_cols:
                        if col not in X_clean.columns:
                            if col == 'Unnamed: 0':
                                X_clean[col] = range(len(X_clean))
                                logging.info(f"Added '{col}' column")
                            else:
                                X_clean[col] = 0
                                logging.warning(f"Added missing column '{col}' with zeros")
                    
                    # Reorder columns to match expected order
                    X_clean = X_clean[expected_cols]
                
                return X_clean
            else:
                return X
                
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, X):
        try:
            # Clean the input data
            X_clean = self._clean_data(X)
            
            # CRITICAL FIX: Convert to numpy array BEFORE transform
            # This bypasses scikit-learn's column name validation
            if hasattr(X_clean, 'values'):
                X_array = X_clean.values
            elif isinstance(X_clean, pd.DataFrame):
                X_array = X_clean.to_numpy()
            else:
                X_array = np.array(X_clean)
            
            logging.info(f"Shape before transform: {X_array.shape}")
            
            # Transform using preprocessor (pass numpy array)
            X_transform = self.preprocessor.transform(X_array)
            
            # Predict
            y_hat = self.model.predict(X_transform)
            return y_hat
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    