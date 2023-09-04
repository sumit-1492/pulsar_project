#stage - 6 : updating components

import os
import sys
import importlib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedShuffleSplit
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories,pickle_file_saving,write_yaml
from pulsarclassification.entity import DataTransformationConfiguration,ModelTrainerConfiguration

class ModelTrainer:
    def __init__(self, 
                 transformation_config: DataTransformationConfiguration,
                 modeltrainer_config: ModelTrainerConfiguration):

        try:
            self.transformation_config = transformation_config
            self.modeltrainer_config = modeltrainer_config
            self.schema = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise PulsarException(e,sys) 
        
    def get_data_for_training(self):
        try:
            model_train_data_file_path = os.path.join(self.transformation_config.transformed_train_dir,TRANSFORMED_MODEL_TRAIN_FILE_NAME)
            model_test_data_file_path = os.path.join(self.transformation_config.transformed_test_dir,TRANSFORMED_MODEL_TEST_FILE_NAME)
            
            model_train_data = pd.read_csv(model_train_data_file_path)
            model_test_data = pd.read_csv(model_test_data_file_path)

            input_features = model_train_data.drop(self.schema.target_column,axis=1)
            logging.info(f"Input features extracted from {TRANSFORMED_MODEL_TRAIN_FILE_NAME} having shape : {input_features.shape} ")
            output_features = model_train_data[self.schema.target_column]
            logging.info(f"Output feature extracted from {TRANSFORMED_MODEL_TRAIN_FILE_NAME} having shape : {output_features.shape} ")
            
            return input_features,output_features

        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_model(self,modellibrary,classificationmodel,modelparameters,inputfeatures,outputfeatures):
        try:
            mllibrary = importlib.import_module(modellibrary)
            mlmodel = getattr(mllibrary, classificationmodel)
            model = mlmodel(**modelparameters)
            model.fit(inputfeatures,outputfeatures)
            return model
        except Exception as e:
            raise PulsarException(e,sys)
    
    def save_model(self):
        try:
            saved_model_artifacts = {SAVED_MODEL_ARTIFACTS_KEY :{}}
            X,y = self.get_data_for_training()  ## X = input features , y = output features

            model_saving_folder_name = os.path.join(self.modeltrainer_config.trained_model_root_dir_name,SAVED_MODEL_FOLDER_KEY)
            create_directories(model_saving_folder_name)

            number_of_model_for_train = []
            for key,value in self.modeltrainer_config.trained_model_selection.items():
                number_of_model_for_train.append(key)

            logging.info(f"Number of model to train : {len(number_of_model_for_train)}")

            for i in range(len(number_of_model_for_train)):

                model_selection = self.modeltrainer_config.trained_model_selection[number_of_model_for_train[i]]
                
                logging.info(f"{model_selection[MODEL_CLASSIFIER_KEY]} training started")
                
                trained_model = self.get_model(model_selection[MODEL_CLASSIFIER_MODULE_KEY],
                                            model_selection[MODEL_CLASSIFIER_KEY],
                                            model_selection[MODEL_CLASSIFIER_PARAMETER_KEY],
                                            X,y)
            
                trained_model_saving_path = os.path.join(model_saving_folder_name,model_selection[MODEL_CLASSIFIER_KEY])
                create_directories(trained_model_saving_path)
                pickle_file_saving(trained_model,trained_model_saving_path,TRAINED_MODEL_FILE_NAME)
                trained_model_path = os.path.join(trained_model_saving_path,TRAINED_MODEL_FILE_NAME)
                key_of_path = f"model_{i}_path_{CURRENT_DATE_STAMP}"
                trained_model_artifacts = {key_of_path:trained_model_path}
                saved_model_artifacts[SAVED_MODEL_ARTIFACTS_KEY].update(trained_model_artifacts)
            
                logging.info(f"{model_selection[MODEL_CLASSIFIER_KEY]} training completed")

            write_yaml(self.modeltrainer_config.trained_model_path_yaml_file,saved_model_artifacts)
            logging.info(f"Model paths updated in yaml file: {self.modeltrainer_config.trained_model_path_yaml_file}")
            
        except Exception as e:
            raise PulsarException(e,sys)