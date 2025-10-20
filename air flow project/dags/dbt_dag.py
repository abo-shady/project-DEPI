from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

DBT_PROJECT_DIR = '/usr/local/airflow/dags/my_dbt_project'

with DAG(
    dag_id='dbt_run_dag',
    start_date=datetime(2025, 9, 29),
    description='A simple DAG to run dbt models',
    schedule=None,  
    catchup=False,
    tags=['dbt'],
) as dag:
    # using connector of dbt to run models
    dbt_run_task = BashOperator(
    task_id='run_dbt_models',
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir ."
)

   
    dag_2 = TriggerDagRunOperator(
        task_id='Train_the_model',
        trigger_dag_id='run_python_script_dag', 
        wait_for_completion=True,  
    )

 
    dbt_run_task >> dag_2