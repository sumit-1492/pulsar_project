import os
import pandas as pd

def read_csv(**context):
    path_print = os.path.join(os.getcwd(),"dags/data/pulsar_train_data.csv")
    dirs_in_path = os.listdir(os.getcwd())
    df = pd.read_csv(path_print)
    save_path = os.path.join(os.getcwd(),"dags/data/pulsar_check.csv")
    df.to_csv(save_path,index=False)
    context['ti'].xcom_push(key='airflow', value={'root_path':os.getcwd(),'path':path_print,'dir':dirs_in_path,'columns':len(df.columns)})