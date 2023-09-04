import os
import sys
from pulsarclassification.config.configuration import ConfigurationManager
from pulsarclassification.components.data_transformation import DataTransformation
from pulsarclassification.exception import PulsarException

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_configuration()
            data_transformation_config = config.get_data_transformation_configuration()
            data_transformation = DataTransformation(validation_config=data_validation_config,
                                            transformation_config=data_transformation_config)
            data_transformation.file_transformation_saving()
        except Exception as e:
            raise PulsarException(e,sys)