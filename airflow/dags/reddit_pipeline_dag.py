import pendulum

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator

import extraction.reddit_service as reddit_service


with DAG(
        'reddit_etl', 
        description='Reddit ETL Python DAG', 
        schedule_interval='20 * * * *', 
        start_date=pendulum.datetime(2022, 7, 1, tz="UTC"), 
        catchup=False,
        tags=['reddit']
    ) as dag:

    python_task	= PythonOperator(
        task_id='extract_posts_data', 
        python_callable=reddit_service.extract_posts_data
    )

python_task
    