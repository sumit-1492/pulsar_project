import os
import sys
import yaml
import pickle
from box.exceptions import BoxValueError
from pulsarclassification.logging import logging
from pulsarclassification.exception import PulsarException
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
        
    except Exception as e:
            raise PulsarException(e,sys)
    
@ensure_annotations
def create_directories(directory_path:str,verbose=True):
    try:
        if (not os.path.exists(directory_path)):
            os.makedirs(directory_path,exist_ok=True)
            if verbose:
                logging.info(f" Directory created in this: {directory_path} ")
        else:
            if verbose:
                logging.info(f" Directory already present: {directory_path} ")

    except Exception as e:
            raise PulsarException(e,sys)
    
@ensure_annotations
def get_file_size(path:Path) -> str:
    try:
        file_size_in_kb = round(os.path.getsize(path)/1024)
        return f"filesize approximately: ~ {file_size_in_kb} KB"
    
    except Exception as e:
            raise PulsarException(e,sys)
  
def pickle_file_saving(model_file,path,saved_file_name) -> str:
    try:
        pickle.dump(model_file,open(os.path.join(path,saved_file_name),'wb'))
        return f"pickle file saved in : {path} "
    
    except Exception as e:
            raise PulsarException(e,sys)
    
def write_yaml(file_path,yaml_data) -> str:
    try:
        with open(file_path,"w") as file:
            yaml.dump(yaml_data, file)
        file.close()
        return f" Model paths saved in  : {file_path}"
    
    except Exception as e:
            raise PulsarException(e,sys)
    

