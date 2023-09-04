import os
import sys
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories
from pulsarclassification.entity import DataIngestionConfiguration,DataValidationConfiguration
from pulsarclassification.entity import DataTransformationConfiguration,ModelTrainerConfiguration
from pulsarclassification.entity import ModelEvaluationConfiguration,ModelPusherConfiguration

class ConfigurationManager:

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        
        try:
            self.config = read_yaml(CONFIG_FILE_PATH)
            create_directories(self.config.artifacts_dir_name)
            logging.info(f" Artifacts directory created at : {self.config.artifacts_dir_name} ")

        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_data_ingestion_config(self) -> DataIngestionConfiguration:

        try:
            artifact_dir = self.config.artifacts_dir_name
            config = self.config.data_ingestion_config

            data_ingestion_dir = os.path.join(artifact_dir,config.root_dir_name)
            create_directories(data_ingestion_dir)

            raw_data_dir = os.path.join(data_ingestion_dir,config.zip_data_dir_name)
            create_directories(raw_data_dir)

            ingested_csv_data_dir = os.path.join(data_ingestion_dir,config.unzip_data_dir_name)
            create_directories(ingested_csv_data_dir)

            data_ingestion_config = DataIngestionConfiguration(
                root_dir_name  = config.root_dir_name,
                dataset_download_url = config.dataset_download_url,
                zip_data_dir_name = raw_data_dir,
                unzip_data_dir_name = ingested_csv_data_dir
            )

            logging.info(f" Data ingestion configuration: {data_ingestion_config}")

            return data_ingestion_config
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_data_validation_configuration(self) -> DataValidationConfiguration:

        try:
            artifact_dir = self.config.artifacts_dir_name
            config = self.config.data_validation_config

            data_validation_dir = os.path.join(artifact_dir,config.validated_root_dir_name)
            create_directories(data_validation_dir)

            data_validation_train_dir = os.path.join(data_validation_dir,config.validated_train_dir)
            create_directories(data_validation_train_dir)

            data_validation_test_dir = os.path.join(data_validation_dir,config.validated_test_dir)
            create_directories(data_validation_test_dir)

            data_validation_config = DataValidationConfiguration(
                validated_root_dir_name  = config.validated_root_dir_name,
                validated_train_dir = data_validation_train_dir,
                validated_test_dir = data_validation_test_dir,
                validated_status_report_file_name = os.path.join(data_validation_dir,config.validated_status_report_file_name),
                validated_required_files = config.validated_required_files
            )

            logging.info(f" Data validation configuration: {data_validation_config}")

            return data_validation_config
        
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_data_transformation_configuration(self) -> DataTransformationConfiguration:

        try:
            artifact_dir = self.config.artifacts_dir_name
            config = self.config.data_transformation_config

            data_transformation_dir = os.path.join(artifact_dir,config.transformed_root_dir_name)
            create_directories(data_transformation_dir)

            data_transformation_train_dir = os.path.join(data_transformation_dir,config.transformed_train_dir)
            create_directories(data_transformation_train_dir)

            data_transformation_test_dir = os.path.join(data_transformation_dir,config.transformed_test_dir)
            create_directories(data_transformation_test_dir)

            data_transformation_industrial_data_dir = os.path.join(data_transformation_dir,config.transformed_industrial_data_dir)
            create_directories(data_transformation_industrial_data_dir)

            data_transformation_preprocess_data_dir = os.path.join(data_transformation_dir,config.transformed_preprocess_dir)
            create_directories(data_transformation_preprocess_data_dir)


            data_transformation_config = DataTransformationConfiguration(
                transformed_root_dir_name = data_transformation_dir,
                transformed_train_dir = data_transformation_train_dir,
                transformed_test_dir =  data_transformation_test_dir,
                transformed_industrial_data_dir =  data_transformation_industrial_data_dir,
                transformed_preprocess_dir = data_transformation_preprocess_data_dir
            )

            logging.info(f" Data transformation configuration: {data_transformation_config}")

            return data_transformation_config
        
        except Exception as e:
            raise PulsarException(e,sys)

    def get_model_trainer_configuration(self) -> ModelTrainerConfiguration:

        try:
            artifact_dir = self.config.artifacts_dir_name
            config = self.config.model_trainer_config
            param_config = read_yaml(MODEL_PARAMETER_FILE_PATH)

            model_trainer_dir = os.path.join(artifact_dir,config.trained_model_root_dir_name)
            create_directories(model_trainer_dir)

            model_trainer_yaml_file = os.path.join(model_trainer_dir,config[MODEL_TRAINER_YAML_FILE_NAME_KEY])

            model_trainer_config = ModelTrainerConfiguration(
                trained_model_root_dir_name = model_trainer_dir,
                trained_model_path_yaml_file = model_trainer_yaml_file,
                trained_model_base_accuracy = config.trained_model_base_accuracy,
                trained_model_overfit_value = config.trained_model_overfit_value,
                trained_model_FPR           = config.trained_model_FPR,
                trained_model_RECALL        = config.trained_model_RECALL,
                trained_model_selection     = param_config[MODEL_SELECTION_KEY]
            )

            logging.info(f" Model trainer configuration: {model_trainer_config}")

            return model_trainer_config
        
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_model_evaluation_configuration(self) -> ModelEvaluationConfiguration:

        try:
            artifact_dir = self.config.artifacts_dir_name
            config = self.config.model_evaluation_config

            model_evaluation_dir = os.path.join(artifact_dir,config.evaluated_model_root_dir_name)
            create_directories(model_evaluation_dir)

            model_evaluated_csv_file = os.path.join(model_evaluation_dir,config[MODEL_EVALUATION_RESULT_FILE_NAME_KEY])

            model_evaluation_config = ModelEvaluationConfiguration(
                evaluated_model_root_dir_name = model_evaluation_dir,
                evaluated_model_result_file_name = model_evaluated_csv_file,
                evaluated_model_result_file_column_name = config.evaluated_model_result_file_column_name
            )

            logging.info(f" Model evaluation configuration: {model_evaluation_config}")

            return model_evaluation_config
        
        except Exception as e:
            raise PulsarException(e,sys)
        
    def get_model_pusher_configuration(self) -> ModelPusherConfiguration:

        try:
            config = self.config.model_pusher_config

            model_pusher_dir = os.path.join(ROOT_DIR,config.pushed_model_root_dir_name)
            create_directories(model_pusher_dir)
            model_pusher_config = ModelPusherConfiguration(
                pushed_model_root_dir_name = model_pusher_dir
            )

            logging.info(f" Model pusher configuration: {model_pusher_config}")

            return model_pusher_config
        
        except Exception as e:
            raise PulsarException(e,sys)