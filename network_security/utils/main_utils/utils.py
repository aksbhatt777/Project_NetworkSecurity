import yaml
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle

def read_yaml(file_path: str) -> dict: #as it is already in the form of key value pair 
    try:
        with open(file_path, "rb") as yaml_file: #binary mode reading
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array): #used in transformation 
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def load_numpy_array(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from network_security.utils.ML_utils.metric.classification_metrics import get_classification_score

def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    "Models and Params will be specified in model trainer"
    try:
        report={}
        for i in range(len(list(models))):        
            model=list(models.values())[i] #takes/initialises models from model-dict values
            print(model)
            param=params[list(models.keys())[i]] #keys of model-dict becomes key call from params-dict
            print(param)

            gs=GridSearchCV(estimator=model,param_grid=param,cv=3)
            gs.fit(X_train,y_train) # training of model using several grids of grid search 

            #get the best params from the grid --> gives best model with best params
            model.set_params(**gs.best_params_) #fetching best params that are in form of dict 
            model.fit(X_train,y_train) #finally training with the best 

            ##could have also done this 
            #model = gs.best_estimator_  # Already trained with best params --> no need to retrain in the model keyword 

            #predictions 
            y_pred_train=model.predict(X_train) # needed to check for underfitting
            y_pred_test=model.predict(X_test) # to check for true performance 

            # # r2score  -- for regression problem 
            # train_model_score = r2_score(y_train, y_pred_train)
            # test_model_score = r2_score(y_test, y_pred_test)
            # report[list(models.keys())[i]] = {
            #     'train_score': train_model_score,
            #     'test_score': test_model_score,
            #     'gap': train_model_score - test_model_score #this gap tell overfitting
            # }

            # Use classification metrics
            train_metric = get_classification_score(y_train, y_pred_train)
            test_metric = get_classification_score(y_test, y_pred_test)
            
            # Store only what we need for selection
            # F1 score as FN will be costly in network security 
            report[list(models.keys())[i]] = {
                'train_score': train_metric.f1_score,  # F1 for training
                'test_score': test_metric.f1_score,    # F1 for testing
                'gap': train_metric.f1_score - test_metric.f1_score
            }

        return report
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
