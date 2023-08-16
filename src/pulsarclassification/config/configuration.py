from pulsarclassification.logging import logging
from pulsarclassification.constants import *
from pulsarclassification.utils.common import read_yaml,create_directories
from pulsarclassification.entity import DataIngestionConfiguration

class ConfigurationManager:

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        
        try:
            self.config = read_yaml(CONFIG_FILE_PATH)
            create_directories(self.config.artifacts_dir_name)
            logging.info(f" Artifacts directory created at : {self.config.artifacts_dir_name} ")

        except  BoxValueError:
            raise ValueError(" Directory path is not present ")
    
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