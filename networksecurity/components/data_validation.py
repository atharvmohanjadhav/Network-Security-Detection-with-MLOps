from networksecurity.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import  SCHEMA_FILE_PATH
from scipy.stats import ks_2samp  # it is for data drift checking
import os,sys
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    @staticmethod  # it is going to use only once
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def validate_number_of_columns(self,df:pd.DataFrame) ->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required no of columns; {number_of_columns}")
            logging.info(f"Data Frama has a columns: {len(df.columns)}")
            if len(df.columns) == number_of_columns:
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def check_data_drift(self,base_df,curr_df,threshold = 0.05)-> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = curr_df[column]
                sample_distribution = ks_2samp(d1,d2)
                if threshold <= sample_distribution.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value": float(sample_distribution.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content= report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_validation(self)->DataIngestionArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            #validate no of columns
            status = self.validate_number_of_columns(df=train_df)
            if not status:
                error_msg = f"Train Dataframe does not contain all columns.\n"

            status = self.validate_number_of_columns(df=test_df)
            if not status:
                error_msg = f"Test Dataframe does not contain all columns.\n"
            
            # check data drift
            status = self.check_data_drift(base_df=train_df,curr_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok= True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,index =False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index =False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path= self.data_validation_config.valid_train_file_path,
                valid_test_file_path= self.data_validation_config.valid_test_file_path,
                invalid_train_file_path= None,
                invalid_test_file_path= None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path


            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
