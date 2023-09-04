import os
import sys
from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.data_ingestion import DataIngestion
from pulsarclassification.exception import PulsarException

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.zip_file_downloader()
            data_ingestion.zip_file_extractor()
        except Exception as e:
            raise PulsarException(e,sys)