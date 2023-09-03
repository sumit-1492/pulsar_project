import os
from pulsarclassification.logging import logging
from pulsarclassification.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from pulsarclassification.pipeline.stage_02_data_validation import DataValidationPipeline
from pulsarclassification.pipeline.stage_03_data_tranformation import DataTransformationPipeline
from pulsarclassification.pipeline.stage_04_model_trainer import ModelTrainerPipeline


#logging.info("checking the log file after changing date time format") #checking of loogging files

STAGE_NAME = " Data Ingestion Stage"
try:
   logging.info(f">>>>>> {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionPipeline()
   data_ingestion.main()
   logging.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
except Exception as e:
        logging.exception(e)
        raise e

STAGE_NAME = " Data Validation Stage"
try:
   logging.info(f">>>>>> {STAGE_NAME} started <<<<<<") 
   data_validation = DataValidationPipeline()
   data_validation.main()
   logging.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
except Exception as e:
        logging.exception(e)
        raise e

STAGE_NAME = " Data Transformation Stage"
try:
   logging.info(f">>>>>> {STAGE_NAME} started <<<<<<") 
   data_transformation = DataTransformationPipeline()
   data_transformation.main()
   logging.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
except Exception as e:
        logging.exception(e)
        raise e

STAGE_NAME = " Model Training Stage"
try:
   logging.info(f">>>>>> {STAGE_NAME} started <<<<<<") 
   model_trainer = ModelTrainerPipeline()
   model_trainer.main()
   logging.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
except Exception as e:
        logging.exception(e)
        raise e