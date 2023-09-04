#stage - 6 : updating components

import os
import sys
import importlib
from sklearn import metrics
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedShuffleSplit
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml
from pulsarclassification.entity import DataTransformationConfiguration,ModelTrainerConfiguration
from pulsarclassification.entity import ModelEvaluationConfiguration
from sklearn.metrics import confusion_matrix,accuracy_score

class ModelEvaluation:
    def __init__(self, 
                 transformation_config: DataTransformationConfiguration,
                 modeltrainer_config: ModelTrainerConfiguration,
                 modelevaluation_config: ModelEvaluationConfiguration):

        try:
            self.transformation_config = transformation_config
            self.modeltrainer_config = modeltrainer_config
            self.modelevaluation_config = modelevaluation_config
            self.schema = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise PulsarException(e,sys) 
        
    def get_data_for_evaluation(self):
        try:
            model_train_data_file_path = os.path.join(self.transformation_config.transformed_train_dir,TRANSFORMED_MODEL_TRAIN_FILE_NAME)
            model_test_data_file_path = os.path.join(self.transformation_config.transformed_test_dir,TRANSFORMED_MODEL_TEST_FILE_NAME)
            
            model_train_data = pd.read_csv(model_train_data_file_path)
            model_test_data = pd.read_csv(model_test_data_file_path)

            train_data_input_features = model_train_data.drop(self.schema.target_column,axis=1)
            logging.info(f"Train data features extracted from {TRANSFORMED_MODEL_TRAIN_FILE_NAME} having shape : {train_data_input_features.shape} ")

            test_data_input_features = model_test_data.drop(self.schema.target_column,axis=1)
            logging.info(f"Test data features extracted from {TRANSFORMED_MODEL_TEST_FILE_NAME} having shape : {test_data_input_features.shape} ")

            train_data_output_features = model_train_data[self.schema.target_column]
            logging.info(f"Output feature extracted from {TRANSFORMED_MODEL_TRAIN_FILE_NAME} having shape : {train_data_output_features.shape} ")

            test_data_output_features = model_test_data[self.schema.target_column]
            logging.info(f"Output feature extracted from {TRANSFORMED_MODEL_TEST_FILE_NAME} having shape : {test_data_output_features.shape} ")
            
            return train_data_input_features,train_data_output_features,test_data_input_features,test_data_output_features

        except Exception as e:
            raise PulsarException(e,sys)
        
    def model_evaluate(self,model,X,y):
        try:
            y_pred = model.predict(X)
            accuracy = accuracy_score(y,y_pred)
            tn,fp,fn,tp = confusion_matrix(y, y_pred, labels=[0, 1]).ravel()
            FPR = fp/(tn+fp)
            RECALL = tp/(tp+fn)
            return accuracy,FPR,RECALL
        except Exception as e:
            raise PulsarException(e,sys)

    def get_model_evaluation_result(self):
        try:
            X_train,y_train,X_test,y_test = self.get_data_for_evaluation()  ## X = input features , y = output features
            saved_model_config = read_yaml(self.modeltrainer_config.trained_model_path_yaml_file)
            print(saved_model_config)
            
            df_result = pd.DataFrame()
            for model_path_key,model_path_name in saved_model_config[SAVED_MODEL_ARTIFACTS_KEY].items():
                result = []
                model = pd.read_pickle(model_path_name)
                train_accuracy,train_fpr,train_recall = self.model_evaluate(model,X_train,y_train)
                test_accuracy,test_fpr,test_recall = self.model_evaluate(model,X_test,y_test)
                result.append(model_path_name)
                result.append(train_accuracy)
                result.append(test_accuracy)
                result.append(train_fpr)
                result.append(test_fpr)
                result.append(train_recall)
                result.append(test_recall)
                model_status = None
                if train_accuracy > self.modeltrainer_config.trained_model_base_accuracy :
                    if (train_accuracy > test_accuracy) and (test_fpr < self.modeltrainer_config.trained_model_FPR) and (test_recall > self.modeltrainer_config.trained_model_RECALL):
                        logging.info(f" All evaluation cases passed ")
                        model_status = 1
                    else:
                        logging.info(f" Evaluation cases failed ")
                        model_status = 0        
                else:
                    logging.info(f" Evaluation cases failed ")
                    model_status = 0
                    
                result.append(model_status)
                temp = pd.DataFrame([result])
                df_result = pd.concat([df_result,temp],axis=0,ignore_index=True)
            df_result.columns = self.modelevaluation_config.evaluated_model_result_file_column_name
            df_result.to_csv(self.modelevaluation_config.evaluated_model_result_file_name,index=False)
            logging.info(f" Model result saved in : {self.modelevaluation_config.evaluated_model_result_file_name} ")
        except Exception as e:
            raise PulsarException(e,sys)