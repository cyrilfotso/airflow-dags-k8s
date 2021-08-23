from airflow.hooks import BashOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
    'start_date': days_ago(3),
}

dag = DAG(
    dag_id='example_bash_operator', default_args=args,
    schedule_interval='@daily')


list_files = BashOperator(
    task_id='list_files', bash_command='ls -l', dag=dag)

task_dag_param = BashOperator(
    task_id='task_dag_param',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag)

python_bash = BashOperator(
    task_id='python_bash',
    bash_command='python ../src/opp_id.py',
    dag=dag)

