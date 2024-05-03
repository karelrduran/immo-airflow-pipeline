from airflow import DAG
from airflow.operators.python import PythonOperator

from app.scraping.do_scrap import scrape

# Scraping apartment and house URLs

# Scraping apartments data

# scraping houses data


from datetime import datetime
default_args = {
    'owner': "karel",
    'email': "karel@ads.com",
    'start_date': datetime(2024, 5, 2),
}

with DAG(
        dag_id='scrape_dag',
        schedule=None,
        catchup=False,
) as dag:
    t1 = PythonOperator(
        task_id='scrape',
        python_callable=scrape
    )
