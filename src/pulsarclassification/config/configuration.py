from pulsarclassification.logging import logging
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories
from pulsarclassification.entity import DataIngestionConfiguration,DataValidationConfiguration

class ConfigurationManager:

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        
        try:
            self.config = read_yaml(CONFIG_FILE_PATH)
            create_directories(self.config.artifacts_dir_name)
            logging.info(f" Artifacts directory created at : {self.config.artifacts_dir_name} ")

        except Exception as e:
            raise e
        
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
            raise e
        
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
            raise e