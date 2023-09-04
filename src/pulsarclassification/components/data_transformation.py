import os
import sys
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedShuffleSplit
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories,get_file_size
from pulsarclassification.entity import DataValidationConfiguration,DataTransformationConfiguration

class DataTransformation:
    def __init__(self, 
                 validation_config:DataValidationConfiguration,
                 transformation_config: DataTransformationConfiguration):

        try:
            self.validation_config = validation_config
            self.transformation_config = transformation_config
            self.schema = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise PulsarException(e,sys)
        
    def file_transformation_saving(self):
        try:
            model_data_file_path = os.path.join(self.validation_config.validated_train_dir,VALIDATED_DATA_FILE_NAME_FOR_MODEL_TRAIN)
            industrial_data_file = os.path.join(self.validation_config.validated_test_dir,VALIDATED_INDUSTRIALDATA_FILE_NAME)
            
            model_data = pd.read_csv(model_data_file_path)
            industrial_data = pd.read_csv(industrial_data_file)

            features = self.schema.feature_columns.split(" ")
            features.remove("id")
            model_data = model_data[features]
            features.remove(self.schema.target_column)
            industrial_data = industrial_data[features]

            sss = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
            model_train_set = None
            model_test_set = None

            for train_index,test_index in sss.split(model_data,model_data['Class']):
                model_train_set = model_data.loc[train_index]
                model_test_set = model_data.loc[test_index]

            model_train_set.reset_index(drop=True,inplace=True)
            model_test_set.reset_index(drop=True,inplace=True)

            model_train_set.to_csv(os.path.join(self.transformation_config.transformed_train_dir,
                                                TRANSFORMED_MODEL_TRAIN_FILE_NAME),index=False)
            logging.info(f"{TRANSFORMED_MODEL_TRAIN_FILE_NAME} saved in {self.transformation_config.transformed_train_dir}")
            model_test_set.to_csv(os.path.join(self.transformation_config.transformed_test_dir,
                                                TRANSFORMED_MODEL_TEST_FILE_NAME),index=False)
            logging.info(f"{TRANSFORMED_MODEL_TEST_FILE_NAME} saved in {self.transformation_config.transformed_test_dir}")
            industrial_data.to_csv(os.path.join(self.transformation_config.transformed_industrial_data_dir,
                                                TRANSFORMED_INDUSTRIALDATA_FILE_NAME),index=False)
            logging.info(f"{TRANSFORMED_INDUSTRIALDATA_FILE_NAME} saved in {self.transformation_config.transformed_industrial_data_dir}")

        except Exception as e:
            raise PulsarException(e,sys)
        