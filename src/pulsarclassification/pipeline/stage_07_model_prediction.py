import os
import sys
import pandas as pd
from pathlib import Path
from pulsarclassification.constants import *
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.utils.common import read_yaml

class InstanceData:
    def __init__(self,
                Mean_Integrated: float,
                SD: float,
                EK: float,
                Skewness: float,
                Mean_DMSNR_Curve: float,
                SD_DMSNR_Curve: float,
                EK_DMSNR_Curve: float,
                Skewness_DMSNR_Curve: float):
        
        try:
            logging.info(f"===============Instance prediction log started===============")
            self.Mean_Integrated = Mean_Integrated
            self.SD = SD
            self.EK = EK
            self.Skewness = Skewness
            self.Mean_DMSNR_Curve = Mean_DMSNR_Curve
            self.SD_DMSNR_Curve = SD_DMSNR_Curve
            self.EK_DMSNR_Curve = EK_DMSNR_Curve
            self.Skewness_DMSNR_Curve = Skewness_DMSNR_Curve
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_instance_data_frame(self):

        try:
            pulsar_instance_input_data = {
                                    "Mean_Integrated": [self.Mean_Integrated],
                                    "SD": [self.SD],
                                    "EK": [self.EK],
                                    "Skewness": [self.Skewness],
                                    "Mean_DMSNR_Curve": [self.Mean_DMSNR_Curve],
                                    "SD_DMSNR_Curve": [self.SD_DMSNR_Curve],
                                    "EK_DMSNR_Curve": [self.EK_DMSNR_Curve],
                                    "Skewness_DMSNR_Curve": [self.Skewness_DMSNR_Curve]
                                   }
            
            df = pd.DataFrame(pulsar_instance_input_data)
            return df
        except Exception as e:
            raise PulsarException(e,sys)
        
class BatchData:

    def __init__(self,batch_csv_file_path:Path):

        try:
            logging.info(f"===============Batch prediction log started===============")
            self.batch_csv_file_path = batch_csv_file_path
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_batch_data_transformation(self):

        try:
            schema = read_yaml(SCHEMA_FILE_PATH)
            config = read_yaml(CONFIG_FILE_PATH)
            artifact_dir = config.artifacts_dir_name
            data_transformation_dir = os.path.join(artifact_dir,config.data_transformation_config.transformed_root_dir_name)
            data_transformation_train_dir = os.path.join(data_transformation_dir,config.data_transformation_config.transformed_train_dir)
            df = pd.read_csv(self.batch_csv_file_path)

            train_data_path = os.path.join(data_transformation_train_dir,TRANSFORMED_MODEL_TRAIN_FILE_NAME)
            train_data = pd.read_csv(train_data_path)

            if df.shape[1] == schema.number_of_feature_columns:
                logging.info(f"Batch data has required number of {schema.number_of_feature_columns} i.e {df.shape}")
                features = schema.feature_columns.split(" ")[:-1]
                df.columns = features
                features.remove("id")
                df = df[features]
                for feature in features:
                    if (df[feature].dtype == schema.datatype_of_columns[feature]):
                        logging.info(f"Batch data has required datatype as train data : {feature}")
                        if df[feature].isna().sum() > 0:
                            logging.info(f"Batch data has null value in:{feature}")
                            df[feature].fillna(train_data[feature].mean(),inplace=True)
                        else:                            
                            logging.info(f"Batch data has no null value in:{feature}")
                    else:
                        logging.info(f"Batch data does not have the required data type")
                        logging.info(f"Please check your data")
                        sys.exit()
            else:
                logging.info(f"Batch data has not required number of {schema.number_of_feature_columns} i.e {df.shape}")
                logging.info(f"Please check your data")
                sys.exit()
            return df
        except Exception as e:
            raise PulsarException(e,sys)
        
class ModelPredict:

    def __init__(self):
        try:
            config = ConfigurationManager()
            self.modelpusher_config = config.get_model_pusher_configuration()
        except Exception as e:
            raise PulsarException(e,sys)

    def predict(self,data):
        try:
            pushed_model_config = read_yaml(self.modelpusher_config.pushed_model_path_yaml_file)
            model = pd.read_pickle(pushed_model_config[PUSHED_MODEL_ARTIFACTS_KEY]['model_path'])
            logging.info(f"latest model read from : {pushed_model_config[PUSHED_MODEL_ARTIFACTS_KEY]['model_path']}")
            result = model.predict(data)
            return result
        except Exception as e:
            raise PulsarException(e,sys)