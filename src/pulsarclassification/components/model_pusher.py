#stage - 6 : updating components

import os
import sys
import importlib
import pandas as pd
from pathlib import Path
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.constants import *
from pulsarclassification.utils.common import pickle_file_saving,write_yaml
from pulsarclassification.entity import ModelEvaluationConfiguration,ModelPusherConfiguration

class ModelPusher:
    def __init__(self, 
                 modelevaluation_config: ModelEvaluationConfiguration,
                 modelpusher_config: ModelPusherConfiguration):

        try:
            self.modelevaluation_config = modelevaluation_config
            self.modelpusher_config = modelpusher_config
        except Exception as e:
            raise PulsarException(e,sys) 
        
    def get_model_pusher(self):
        try:
           pushed_model_artifacts = {PUSHED_MODEL_ARTIFACTS_KEY :{}}
           result_file = pd.read_csv(self.modelevaluation_config.evaluated_model_result_file_name)
           result_status_file = result_file[result_file[PUSHED_MODEL_STATUS_FEATURE_NAME] == 1] ## 1 represent it passed all the status measures
           max_value_of_required_metric = result_status_file[PUSHED_MODEL_METRIC_EVALUATION_FEATURE_NAME].max()
           required_model_path = result_status_file[result_status_file[PUSHED_MODEL_METRIC_EVALUATION_FEATURE_NAME]== max_value_of_required_metric][PUSHED_MODEL_FILE_PATH_FEATURE_NAME].values[0]
           logging.info(f" {required_model_path} has best test accuracy amomg all the trained models i.e {max_value_of_required_metric}")
           final_model = pd.read_pickle(required_model_path)
           pickle_file_saving(final_model,self.modelpusher_config.pushed_model_root_dir_name,PUSHED_MODEL_FILE_NAME_KEY)
           logging.info(f"Final model saved in : {self.modelpusher_config.pushed_model_root_dir_name}")
           key_of_path = "model_path"
           pushed_model_path = os.path.join(self.modelpusher_config.pushed_model_root_dir_name,PUSHED_MODEL_FILE_NAME_KEY)
           model_artifact = {key_of_path:pushed_model_path}
           pushed_model_artifacts[PUSHED_MODEL_ARTIFACTS_KEY].update(model_artifact)
           write_yaml(self.modelpusher_config.pushed_model_path_yaml_file,pushed_model_artifacts)
           logging.info(f"Pushed model paths updated in yaml file: {self.modelpusher_config.pushed_model_path_yaml_file}")
        except Exception as e:
            raise PulsarException(e,sys)