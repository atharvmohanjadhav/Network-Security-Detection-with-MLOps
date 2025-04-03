import os,sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object,load_object,load_np_array,evaluate_model
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier)
import mlflow

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact = DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def track_mlflow(self,best_model,classification_train_metric): 
        with mlflow.start_run():

            f1_score = classification_train_metric.f1_score
            precision_score = classification_train_metric.precision_score
            recall_score = classification_train_metric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            mlflow.sklearn.log_model(best_model,'model')



    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            "Random Forest":RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost":AdaBoostClassifier()
        }
        params = {
            "Decision Tree" :{
                "criterion":['gini','entropy','log_loss']
            },
            "Random Forest":{
                "n_estimators":[8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                "learning_rate":[.1,.01,.05,.001],
                "subsample": [0.6,0.7,0.75,0.8,0.85,0.9],
                "n_estimators":[8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
               "learning_rate":[.1,.01,.05,.001],
               "n_estimators":[8,16,32,64,128,256] 
            }
        }
        model_report:dict = evaluate_model(x_train,y_train,x_test,y_test,models=models,params=params)

        # to get best model score
        best_model_name = max(model_report, key=model_report.get)
        best_model_score = model_report[best_model_name]

        # to get best model from models dictionary
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)
        
        classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        # to track MLflow
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)

        preproessor = load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        # this is for transformation and prediction
        network_model = NetworkModel(preprocessor=preproessor,model= best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=network_model)

        # model trainer artifact
        model_training_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_atifact=classification_test_metric)
        
        logging.info(f"Model training Artifact: {model_training_artifact}")
         

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #load np array
            train_arr = load_np_array(train_file_path)
            test_arr = load_np_array(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model = self.train_model(x_train,y_train,x_test,y_test)

        except Exception as e:
            raise NetworkSecurityException(e,sys)