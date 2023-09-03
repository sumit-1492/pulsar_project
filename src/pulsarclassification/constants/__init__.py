import os
from pathlib import Path
from datetime import datetime

ROOT_DIR = os.getcwd()
CURRENT_DATE_STAMP = f"{datetime.now().strftime('%d%m%Y')}"

## config file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)

# Data Ingestion related variable

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR_KEY = "root_dir_name"
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "zip_data_dir_name"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "unzip_data_dir_name"

INGESTED_TRAIN_FILE_NAME = "train.csv"
INGESTED_TEST_FILE_NAME = "test.csv"

# Data validation related variable

SCHEMA_FILE_NAME = "schema.yaml"
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,SCHEMA_FILE_NAME)

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR_NAME_KEY = "validated_root_dir_name"
DATA_VALIDATION_TRAIN_DIR_NAME_KEY = "validated_train_dir"
DATA_VALIDATION_TEST_DIR_NAME_KEY = "validated_test_dir"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "status_report_file_name"
DATA_VALIDATION_REQUIRE_KEY = "validated_required_files"

VALIDATED_DATA_FILE_NAME_FOR_MODEL_TRAIN = 'pulsar.csv'
VALIDATED_INDUSTRIALDATA_FILE_NAME = 'Industrial_pulsar_data.csv'

# Data transformation related variable

DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR_NAME_KEY = "transformed_root_dir_name"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_INDUSTRIAL_DATA_NAME_KEY = "transformed_industrial_data_dir"
DATA_TRANSFORMATION_PREPROCESS_DIR_NAME_KEY = "transformed_preprocess_dir"

TRANSFORMED_PICKLE_FILE_NAME = 'data_preprocess.pkl'
TRANSFORMED_MODEL_TRAIN_FILE_NAME = 'pulsar_train_data.csv'
TRANSFORMED_MODEL_TEST_FILE_NAME = 'pulsar_test_data.csv'
TRANSFORMED_INDUSTRIALDATA_FILE_NAME = 'Industrial_pulsar_data.csv'

## Model train related variable

MODEL_PARAMETER_FILE_NAME = "params.yaml"
MODEL_PARAMETER_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,MODEL_PARAMETER_FILE_NAME)

MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR_NAME_KEY = "trained_model_root_dir_name"
MODEL_TRAINER_YAML_FILE_NAME_KEY = "trained_model_path_yaml_file"
MODEL_TRAINER_BASE_ACCURACY_KEY = "trained_model_base_accuracy"
MODEL_TRAINER_OVERFIT_VALUE_KEY = "trained_model_overfit_value"
MODEL_TRAINER_FPR_KEY = "trained_model_FPR"
MODEL_TRAINER_RECALL_KEY = "trained_model_RECALL"

MODEL_SELECTION_KEY = 'model_selection'
MODEL_CLASSIFIER_KEY = 'classifier'
MODEL_CLASSIFIER_MODULE_KEY = 'module'
MODEL_CLASSIFIER_PARAMETER_KEY = 'params'

SAVED_MODEL_FOLDER_KEY = f"model_{CURRENT_DATE_STAMP}"
SAVED_MODEL_ARTIFACTS_KEY = "all_trained_model_paths"
TRAINED_MODEL_FILE_NAME = "model.pkl"

## Model evaluation related variable

MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_ARTIFACT_DIR_NAME_KEY = "evaluated_model_root_dir_name"
MODEL_EVALUATION_RESULT_FILE_NAME_KEY = "evaluated_model_result_file_name"
MODEL_EVALUATION_RESULT_FILE_COLUMN_NAME_KEY = "evaluated_model_result_file_column_name"

