import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import dill
import pickle
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path: str) ->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def write_yaml_file(file_path:str,content:object,replace:bool = False)-> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
            
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_np_array(file_path:str,array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok= True)
        with open(file_path,"wb") as file:
            np.save(file,array)
            
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str , obj:object) ->None:
    try:
        logging.info("Entered the save object method of Utils Class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(obj,file)
        logging.info("Exited the save object method of Main Utils class!")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The {file_path} not exist!")
        with open(file_path,"rb") as file:
            print(file)
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_np_array(file_path:str) ->  np.array:   # load numpy array from file location
    try:
        with open(file_path,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report 

    except Exception as e:
        raise NetworkSecurityException(e,sys)