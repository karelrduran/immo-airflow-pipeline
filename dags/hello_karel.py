from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'owner': "karel",
    'email': "karel@ads.com",
    'start_date': datetime(2020, 1, 1),
}

with DAG('hello_karel', default_args=default_args) as dag:
    t2 = BashOperator(
        task_id='t1',
        bash_command='echo hello karel',
    )
