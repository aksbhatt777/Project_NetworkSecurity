import os
import sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import ModelTrainerConfig #output_config
from network_security.entity.artifact_entity import DataTransformationArtifact #input
from network_security.entity.artifact_entity import ModelTrainerArtifact #output loci

#importing classes for utils
from network_security.utils.main_utils.utils import save_object,load_object,load_numpy_array,evaluate_models
from network_security.utils.ML_utils.metric.classification_metrics import get_classification_score
from network_security.utils.ML_utils.model.estimator import NetworkModel

#sklearn models 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier

#Mlfow and dagshub 
import mlflow
#from urllib.parse import urlparse

#with this mlflow goes to dagshub
import dagshub
dagshub.init(repo_owner='aksbhatt777', repo_name='Project_NetworkSecurity', mlflow=True)


## main working 
class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact #inputs here
            self.model_trainer_config=model_trainer_config 
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def train_model(self,X_train,y_train,X_test,y_test):

        models= {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }# values are the models being initialised in 'models' variable looping

        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                 'splitter':['best','random'],
                # 'max_features':['sqrt','log2']
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],                
                 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            } 
        }

        model_report:dict=evaluate_models(X_train,y_train,X_test,y_test,models,params) #return type is dict 
        #model report will be a nested dict - {modelname : {trainscore , test score , gap }} 

        #best model needs to be max test score and min gap 
        #here considering only test score ... Best F1 score here
        #max with 2 params - iterable,key
        best_model_name=max(model_report.keys(),key=lambda k: model_report[k]['test_score'])
        best_model = models[best_model_name] 

        #getting predictions
        y_pred_train=best_model.predict(X_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_pred_train)
        y_pred_test=best_model.predict(X_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_pred_test) 
        #Both metric sent to artifact later 

        # Log with MLflow (F1, Precision, Recall)
        self.track_mlflow(best_model, classification_train_metric) #log mlflow for train
        self.track_mlflow(best_model, classification_test_metric) #log mlflow for test

        # Now for building complete model pipeline we reload preprocessor 
        preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        #combine preprocessor with best model
        Network_Model=NetworkModel(preprocessor,best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model) 
        # This wrapper works on production level on new unseen data 

        #model pusher
        save_object("final_model/model.pkl",best_model)

        #put all in artifact 
        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def track_mlflow(self,best_model,classificationmetric):
        # mlflow.set_registry_uri("")
        # tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            # Extract metrics
            f1_score=classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score

            # Log metrics
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            # log model
            mlflow.sklearn.log_model(best_model, "model")

            # If remote tracking, register model
            # if tracking_url_type_store != "file":
            #     mlflow.sklearn.log_model(
            #         best_model, 
            #         "model", 
            #         registered_model_name=best_model  # ❌ BUG!
            #     )
            # else:
            #     mlflow.sklearn.log_model(best_model, "model")


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        "Ties all together"
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
