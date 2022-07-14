import pendulum

from airflow.decorators import dag, task

import extraction.reddit_service as reddit_service
import extraction.google_sheets_service as google_sheets_service


@dag(
    description='Reddit ETL Python DAG', 
    schedule_interval='0 0 * * *', 
    start_date=pendulum.datetime(2022, 7, 1, tz="UTC"), 
    catchup=False,
    tags=['reddit']
)
def reddit_etl():

    @task(task_id='extract_posts_data')
    def extract_posts():
        return reddit_service.extract_posts_data()

    @task(task_id='transform_posts_data')
    def transform_posts(extracted_data_list: list):
        return reddit_service.transform_posts(extracted_data_list)

    @task(task_id='save_data_locally')
    def save_to_csv(posts_list: list):
        reddit_service.save_to_csv(posts_list)

    @task(task_id='save_to_google_sheets')
    def upload_to_gsheets(posts_list: list):
        google_sheets_service.upload(posts_list)

    extracted_posts_list = extract_posts()
    transformed_posts_list = transform_posts(extracted_posts_list)
    save_to_csv(transformed_posts_list)
    upload_to_gsheets(transformed_posts_list)


reddit_etl_dag = reddit_etl()
