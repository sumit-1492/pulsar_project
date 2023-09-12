from dataclasses import dataclass 
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfiguration:

    root_dir_name: Path
    dataset_download_url: str
    zip_data_dir_name: Path
    unzip_data_dir_name: Path

@dataclass(frozen=True)
class DataValidationConfiguration:

    validated_root_dir_name: Path
    validated_train_dir: Path
    validated_test_dir: Path
    validated_status_report_file_name: str
    validated_required_files:list

@dataclass(frozen=True)
class DataTransformationConfiguration:

    transformed_root_dir_name: Path
    transformed_train_dir: Path
    transformed_test_dir: Path
    transformed_industrial_data_dir: Path
    transformed_preprocess_dir: Path

@dataclass(frozen=True)
class ModelTrainerConfiguration:

    trained_model_root_dir_name: Path
    trained_model_path_yaml_file: str
    trained_model_base_accuracy: float
    trained_model_overfit_value: float
    trained_model_FPR: float
    trained_model_RECALL: float
    trained_model_selection:str

@dataclass(frozen=True)
class ModelEvaluationConfiguration:

    evaluated_model_root_dir_name: Path
    evaluated_model_result_file_name: str
    evaluated_model_result_file_column_name: list

@dataclass(frozen=True)
class ModelPusherConfiguration:

    pushed_model_root_dir_name:Path
    pushed_model_information_dir_name: Path
    pushed_model_path_yaml_file: str
