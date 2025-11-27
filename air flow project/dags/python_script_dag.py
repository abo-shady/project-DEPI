from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

PYTHON_SCRIPT_PATH = r'C:\Users\medos\Downloads\project-DEPI\air flow project\dags\scripts\python.py'

with DAG(
    dag_id='run_python_script_dag',
    start_date=datetime(2025, 9, 29),
    description='A simple DAG to run a Python script',
    schedule=None, 
    catchup=False,
    tags=['python', 'scripts'],
) as dag:
    
    run_script_task = BashOperator(
    task_id='run_my_python_script',
    bash_command=f"python {PYTHON_SCRIPT_PATH}"
)