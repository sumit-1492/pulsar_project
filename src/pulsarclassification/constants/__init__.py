import os
from pathlib import Path

ROOT_DIR = os.getcwd()

## config file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)

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
SCHEMA_FILE_PATH = os.path.join(CONFIG_FOLDER_NAME,SCHEMA_FILE_NAME)

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR_NAME_KEY = "validated_root_dir_name"
DATA_VALIDATION_TRAIN_DIR_NAME_KEY = "validated_train_dir"
DATA_VALIDATION_TEST_DIR_NAME_KEY = "validated_test_dir"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "status_report_file_name"
DATA_VALIDATION_REQUIRE_KEY = "validated_required_files"

VALIDATED_DATA_FILE_NAME_FOR_MODEL_TRAIN = 'pulsar.csv'
VALIDATED_INDUSTRIALDATA_FILE_NAME = 'Industrial_pulsar_data.csv'
