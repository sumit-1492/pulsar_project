import os
import sys
from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.data_validation import DataValidation
from pulsarclassification.exception import PulsarException

class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_configuration = config.get_data_ingestion_config()
            data_validation_config = config.get_data_validation_configuration()
            data_validation = DataValidation(ingestion_config=data_ingestion_configuration,
                                            validation_config=data_validation_config)
            data_validation.file_exist_validation()
            data_validation.number_of_columns_validation()
            data_validation.datatype_of_columns_validation()
            data_validation.null_value_of_columns_validation()
            data_validation.unique_value_of_columns_validation()
            data_validation.saving_validated_data()
        except Exception as e:
            raise PulsarException(e,sys)