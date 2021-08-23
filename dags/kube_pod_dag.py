"""
This is an example dag for using the Kubernetes Executor.
"""
import os

from airflow import DAG
from airflow.example_dags.libs.helper import print_stuff
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='example_kubernetes_executor',
    default_args=args,
    schedule_interval='@daily',
    start_date=days_ago(2),
    tags=['example', 'example2'],
) as dag:

    affinity = {
        'podAntiAffinity': {
            'requiredDuringSchedulingIgnoredDuringExecution': [
                {
                    'topologyKey': 'kubernetes.io/hostname',
                    'labelSelector': {
                        'matchExpressions': [{'key': 'app', 'operator': 'In', 'values': ['airflow']}]
                    },
                }
            ]
        }
    }

    tolerations = [{'key': 'dedicated', 'operator': 'Equal', 'value': 'airflow'}]

    def assert_zip_binary():
        """
        Checks whether Zip is installed.
        :raises SystemError: if zip is not installed
        """
        return_code = os.system("zip")
        if return_code != 0:
            raise SystemError("The zip binary is not found")


    def my_func(**kwargs):
        print(kwargs)
        print('return from dag run zero')
        return kwargs['param_1']

    # You don't have to use any special KubernetesExecutor configuration if you don't want to
    start_task = PythonOperator(task_id="start_task", python_callable=print_stuff)

    zero_task = PythonOperator(
        task_id="zero_task",
        python_callable=my_func,
        op_kwargs={'param_1': 'one', 'param_2': 'two', 'param_3': 'three'},
        executor_config={"KubernetesExecutor": {"labels": {"foo": "bar"}}},
    )
    # But you can if you want to
    one_task = PythonOperator(
        task_id="one_task",
        python_callable=my_func,
        op_kwargs={'param_1': 'one', 'param_2': 'two', 'param_3': 'three'},
        executor_config={"KubernetesExecutor": {"image": "airflow/ci:latest"}},
    )

    # Use the zip binary, which is only found in this special docker image
    two_task = PythonOperator(
        task_id="two_task",
        python_callable=assert_zip_binary,
        executor_config={"KubernetesExecutor": {"image": "airflow/ci_zip:latest"}},
    )

    # Limit resources on this operator/task with node affinity & tolerations
    three_task = PythonOperator(
        task_id="three_task",
        python_callable=print_stuff,
        executor_config={
            "KubernetesExecutor": {
                "request_memory": "128Mi",
                "limit_memory": "128Mi",
                "tolerations": tolerations,
                "affinity": affinity,
            }
        },
    )

    # Add arbitrary labels to worker pods
    four_task = PythonOperator(
        task_id="four_task",
        python_callable=print_stuff,
        executor_config={"KubernetesExecutor": {"labels": {"foo": "bar"}}},
    )

    start_task >> [zero_task, one_task, two_task, three_task, four_task]