import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from checkdags.checkpython import read_csv

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 10, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=20),
}

dag = DAG("check_dag", default_args=default_args, schedule_interval=timedelta(minutes = 1))


with DAG(dag_id="check_dag", schedule_interval="@once", default_args=default_args, catchup=False) as dag:

    read_file = PythonOperator(task_id="read_csv",python_callable=read_csv)

read_file