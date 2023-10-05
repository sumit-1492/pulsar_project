FROM apache/airflow:2.7.0

ARG CURRENT_USER=$USER
USER root
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3.9-distutils python3.9-dev build-essential
USER airflow

COPY ./dags /opt/airflow/dags
COPY ./requirements.txt /opt/airflow/requirements.txt
COPY ./src/pulsarclassification /opt/airflow/dags/pulsarclassification
COPY ./config /opt/airflow/config

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
RUN airflow db init
RUN airflow users create --role Admin --username sumit --email sumit58kumar@gmial.com --firstname sumit --lastname sahoo --password sumitkumar58
