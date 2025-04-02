import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import dill
import pickle
import numpy as np

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