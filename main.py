import os
from pulsarclassification.logging import logging
from pulsarclassification.pipeline.stage_01_data_ingestion import DataIngestionPipeline


#logging.info("checking the log file after changing date time format") #checking of loogging files

STAGE_NAME = " Data Ingestion Stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionPipeline()
   data_ingestion.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e