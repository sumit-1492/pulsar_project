import os
import sys
from pulsarclassification.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from pulsarclassification.pipeline.stage_02_data_validation import DataValidationPipeline
from pulsarclassification.pipeline.stage_03_data_tranformation import DataTransformationPipeline
from pulsarclassification.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from pulsarclassification.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline
from pulsarclassification.pipeline.stage_06_model_pusher import ModelPusherPipeline

def data_ingestion(**context):
    STAGE_NAME = " Data Ingestion Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='data_ingestion', value=STAGE_NAME)

def data_validation(**context):
    STAGE_NAME = " Data Validation Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    data_validation = DataValidationPipeline()
    data_validation.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='data_validation', value=STAGE_NAME)

def data_transformation(**context):
    STAGE_NAME = " Data Transformation Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='data_transformation', value=STAGE_NAME)

def model_trainer(**context):
    STAGE_NAME = " Model Training Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    model_trainer = ModelTrainerPipeline()
    model_trainer.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='model_trainer', value=STAGE_NAME)

def model_evaluation(**context):
    STAGE_NAME = " Model Evaluation Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    model_evaluator = ModelEvaluationPipeline()
    model_evaluator.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='model_evaluation', value=STAGE_NAME)

def model_pusher(**context):
    STAGE_NAME = " Model Pusher Stage"
    print(f">>>>>> {STAGE_NAME} started <<<<<<") 
    model_pusher = ModelPusherPipeline()
    model_pusher.main()
    print(f">>>>>> {STAGE_NAME} completed <<<<<<\n\n[x==================================================x")
    context['ti'].xcom_push(key='model_pusher', value=STAGE_NAME)






