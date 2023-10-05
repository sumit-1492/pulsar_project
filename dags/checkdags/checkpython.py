import yaml
import os
import pandas as pd

def read_csv(**context):
    path_print = os.path.join(os.getcwd(),"dags/data/pulsar_train_data.csv")
    dirs_in_path = os.listdir(os.getcwd())
    dirs_in_dags = os.listdir(os.path.join(os.getcwd(),'dags'))
    df = pd.read_csv(path_print)
    print(df.head())
    save_path = os.path.join(os.getcwd(),"dags/data/pulsar_check.csv")
    df.to_csv(save_path,index=False)
    pulsarclassification_path = os.path.join(os.getcwd(),'dags',"pulsarclassification")
    pulsar_dir = os.listdir(pulsarclassification_path)
    requirement_path = os.path.join(os.getcwd(),"requirements.txt")
    with open(requirement_path) as file:
        lines = file.readlines()
        print(lines)
    config_path = os.path.join(os.getcwd(),"config")
    config_dir = os.listdir(config_path)
    config_yaml_path = os.path.join(config_path,"config.yaml")
    with open(config_yaml_path) as file:
            yaml_file_content = yaml.safe_load(file)
    print(yaml_file_content)
    context['ti'].xcom_push(key='airflow', value={'root_path':os.getcwd(),
                                                  'path':path_print,
                                                  'dir':dirs_in_path,
                                                  'dag_dir':dirs_in_dags,
                                                  #'pulsar_path':pulsarclassification_path,
                                                  #'pulsar_dir':pulsar_dir,
                                                  #'config_path':config_path,
                                                  #'config_dir':config_dir,
                                                  #'columns':len(df.columns)
                                                    })
    
#'pulsar_path':pulsarclassification_path,
#'pulsar_dir':pulsar_dir,
#'columns':len(df.columns)