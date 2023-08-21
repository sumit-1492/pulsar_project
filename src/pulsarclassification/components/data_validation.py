import os
import pandas as pd
from pathlib import Path
from pulsarclassification.logging import logging
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories,get_file_size
from pulsarclassification.entity import DataIngestionConfiguration,DataValidationConfiguration

class DataValidation:
    def __init__(self, ingestion_config : DataIngestionConfiguration,
                 validation_config:DataValidationConfiguration):

        try:
            self.ingestion_config = ingestion_config
            self.validation_config = validation_config
            self.schema = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise e 
        
    def file_exist_validation(self):
        try:
            file_exist_status = None
            all_files = os.listdir(self.ingestion_config.unzip_data_dir_name)
            with open(self.validation_config.validated_status_report_file_name,'w') as f:
                f.write(f">>>>>>>>>>>>file exist validation<<<<<<<<<<<<<\n\n")
                for file in all_files:
                    if file not in all_files:
                        file_exist_status = False
                        f.write(f"Validation status: {file_exist_status}------->{file} not present\n\n")
                    else:
                        file_exist_status = True
                        f.write(f"Validation status: {file_exist_status}------->{file} is present\n\n")
            f.close()
            logging.info(f"Validation status updated: {self.validation_config.validated_status_report_file_name}")
            return file_exist_status
        except Exception as e:
            raise e
        
    def number_of_columns_validation(self):
        try:
            vs = None
            train_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TRAIN_FILE_NAME)
            test_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TEST_FILE_NAME)
            
            df_train = pd.read_csv(train_data_file)
            df_test = pd.read_csv(test_data_file)

            df_train.drop(columns=self.schema.target_column,inplace=True)
            with open(self.validation_config.validated_status_report_file_name,'a') as f:
                f.write(f">>>>>>>>>>>>number of column validation<<<<<<<<<<<<<\n\n")
                if df_train.shape[1] == self.schema.number_of_feature_columns:
                        vs = True
                        f.write(f"Validation status:{vs}-------> Training file has {self.schema.number_of_feature_columns} columns\n\n")
                else:
                    vs = False
                    f.write(f"Validation status:{vs}-------> Training file has {df_train.shape[1]} columns\n\n")

                if df_test.shape[1] == self.schema.number_of_feature_columns:
                        vs = True
                        f.write(f"Validation status:{vs}-------> Industrial test file has {self.schema.number_of_feature_columns} columns\n\n")
                else:
                    vs = False
                    f.write(f"Validation status:{vs}-------> Industrial test file has {df_train.shape[1]} columns\n\n")
            f.close()
            logging.info(f"Validation status updated: {self.validation_config.validated_status_report_file_name}")
            return vs
        except Exception as e:
            raise e
        
    def datatype_of_columns_validation(self):
        try:
            vs = None
            train_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TRAIN_FILE_NAME)
            test_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TEST_FILE_NAME)
            
            df_train = pd.read_csv(train_data_file)
            df_test = pd.read_csv(test_data_file)

            features_list = df_test.columns.to_list()
            with open(self.validation_config.validated_status_report_file_name,'a') as f:
                f.write(f">>>>>>>>>>>>datatype of column validation<<<<<<<<<<<<<\n\n")
                for feature in features_list:
                    if (df_train[feature].dtype == self.schema.datatype_of_columns[feature]) and (df_test[feature].dtype == self.schema.datatype_of_columns[feature]) :
                            vs = True
                            f.write(f"Validation status:{vs}-------> The {feature} is present in Training file and Industrial test file has datatype {self.schema.datatype_of_columns[feature]} \n\n")
                    else:
                        vs = False
                        f.write(f"Validation status:{vs}-------> The {feature} is not present in Training file and Industrial test file. Please check this {feature} \n\n")
                if df_train[self.schema.target_column].dtype == self.schema.datatype_of_columns[self.schema.target_column]:
                    vs = True
                    f.write(f"Validation status:{vs}-------> The target column i.e {self.schema.target_column} is present in train file\n\n")
                else:
                    vs = False
                    f.write(f"Validation status:{vs}-------> The target column i.e {self.schema.target_column} is not present in train file\n\n")
            f.close()
            logging.info(f"Validation status updated: {self.validation_config.validated_status_report_file_name}")
            return vs
        except Exception as e:
            raise e
        
    def null_value_of_columns_validation(self):
        try:
            vs = None
            train_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TRAIN_FILE_NAME)
            test_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TEST_FILE_NAME)
            
            df_train = pd.read_csv(train_data_file)
            df_test = pd.read_csv(test_data_file)
            train_status = df_train.isna().sum().sum()
            test_status = df_test.isna().sum().sum()
            with open(self.validation_config.validated_status_report_file_name,'a') as f:
                f.write(f">>>>>>>>>>>>null value of column validation<<<<<<<<<<<<<\n\n")
                if train_status == test_status == 0:
                        vs = True
                        f.write(f"Validation status:{vs}-------> The is no null value in train and industrial test data\n\n")
                elif train_status != 0:
                    vs = False
                    null_features = [feature for feature in df_train.columns if df_train[feature].isna().sum()>0]
                    f.write(f"Validation status:{vs}-------> These features {null_features} have null value in train file \n\n")
                elif test_status != 0:
                    vs = False
                    null_features = [feature for feature in df_test.columns if df_test[feature].isna().sum()>0]
                    f.write(f"Validation status:{vs}-------> These features {null_features} have null value in industrial test file \n\n")
            f.close()
            logging.info(f"Validation status updated: {self.validation_config.validated_status_report_file_name}")
            return vs
        except Exception as e:
            raise e
        
    def unique_value_of_columns_validation(self):
        try:
            train_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TRAIN_FILE_NAME)
            test_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TEST_FILE_NAME)
            
            df_train = pd.read_csv(train_data_file)
            df_test = pd.read_csv(test_data_file)
            
            with open(self.validation_config.validated_status_report_file_name,'a') as f:
                f.write(f">>>>>>>>>>>>unique value of each column<<<<<<<<<<<<<\n\n")
                f.write(f">>>>>>>>>>>>unique value of each column in train data<<<<<<<<<<<<<\n\n")
                f.write(f"shape of traing data : {df_train.shape}\n\n")
                for feature in df_train.columns:
                        f.write(f"{feature} has {df_train[feature].nunique()} unique values \n\n")

                f.write(f">>>>>>>>>>>>unique value of each column in industrial test data<<<<<<<<<<<<<\n\n")
                f.write(f"shape of industrial test  data : {df_test.shape}\n\n")
                for feature in df_test.columns:
                        f.write(f"{feature} has {df_test[feature].nunique()} unique values \n\n") 
            f.close()
            logging.info(f"Validation status updated: {self.validation_config.validated_status_report_file_name}")
        except Exception as e:
            raise e
        
    def saving_validated_data(self):
        try:
            train_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TRAIN_FILE_NAME)
            test_data_file = os.path.join(self.ingestion_config.unzip_data_dir_name,INGESTED_TEST_FILE_NAME)
            
            df_train = pd.read_csv(train_data_file)
            df_test = pd.read_csv(test_data_file)

            validated_training_data_file_path = os.path.join(self.validation_config.validated_train_dir,VALIDATED_DATA_FILE_NAME_FOR_MODEL_TRAIN)
            validated_industrial_test_data_file_path = os.path.join(self.validation_config.validated_test_dir,VALIDATED_INDUSTRIALDATA_FILE_NAME)

            df_train.to_csv(validated_training_data_file_path,index=False)
            df_test.to_csv(validated_industrial_test_data_file_path,index=False)
            
            logging.info(f"Validated train data saved in : {validated_training_data_file_path}")
            logging.info(f"Validated industrial test data saved in : {validated_industrial_test_data_file_path}")
            
        except Exception as e:
            raise e