import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pipeline_functions import data_ingestion,data_validation,data_transformation
from pipeline_functions import model_trainer,model_evaluation,model_pusher

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

dag = DAG("pipeline_schedule", default_args=default_args, schedule_interval=timedelta(seconds = 30))

with DAG(dag_id="pipeline_schedule", schedule_interval="@once", default_args=default_args, catchup=False) as dag:

    ingestion = PythonOperator(task_id="data_ingestion",python_callable=data_ingestion,provide_context=True,)
    validation = PythonOperator(task_id="data_validation",python_callable=data_validation,provide_context=True,)
    transformation = PythonOperator(task_id="data_transformation",python_callable=data_transformation,provide_context=True,)

    trainer = PythonOperator(task_id="model_trainer",python_callable=model_trainer,provide_context=True,)
    evaluation = PythonOperator(task_id="model_evaluation",python_callable=model_evaluation,provide_context=True,)
    pusher = PythonOperator(task_id="model_pusher",python_callable=model_pusher,provide_context=True,)

ingestion >> validation
validation >> transformation
transformation >> trainer
trainer >> evaluation
evaluation >> pusher