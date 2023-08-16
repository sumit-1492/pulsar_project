import os
import yaml
from box.exceptions import BoxValueError
from pulsarclassification.logging import logging
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(yaml_file_path:str)->ConfigBox:

    try:
        with open(yaml_file_path) as file:
            yaml_file_content = yaml.safe_load(file)
            logging.info(f" yaml file from this path {yaml_file_path} read succesfully")
            return ConfigBox(yaml_file_content)
        
    except  BoxValueError:
        raise ValueError("yaml file is empty")
    
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(directory_path:str,verbose=True):
    try:
        os.makedirs(directory_path,exist_ok=True)
        if verbose:
            logging.info(f" Directory created in this: {directory_path} ")

    except  BoxValueError:
        raise ValueError(" Directory path is not present ")
    
    except Exception as e:
        raise e
    
@ensure_annotations
def get_file_size(path:Path) -> str:
    try:
        file_size_in_kb = round(os.path.getsize(path)/1024)
        return f"filesize approximately: ~ {file_size_in_kb} KB"
    
    except  BoxValueError:
        raise ValueError(" path is not present ")
    
    except Exception as e:
        raise e
    

