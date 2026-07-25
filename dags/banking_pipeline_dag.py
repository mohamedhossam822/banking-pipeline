import textwrap
from datetime import datetime, timedelta

from airflow.providers.standard.operators.bash import BashOperator

from airflow.sdk import DAG

doc_md ="""
    This is a simple banking pipeline DAG that generates synthetic banking data, validates it, and loads it into a database.
    """  

with DAG(
    "banking_pipeline_dag",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1)
    },
    description="A simple banking pipeline DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["pipeline", "banking"],
) as dag:
    dag.doc_md =doc_md

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="generate_data",
        bash_command="python /opt/airflow/scripts/generate_data.py",
    )
    t1.doc_md = textwrap.dedent(
        """
        #### Task Documentation
        This is a task to generate synthetic banking data using the `generate_data.py` script.
        """
    )

    t2 = BashOperator(
        task_id="validate_data",
        bash_command="python /opt/airflow/scripts/validate_data.py"
    )
    t2.doc_md = textwrap.dedent(
        """
        #### Task Documentation
        This is a task to validate the generated banking data using the `validate_data.py` script.
        """
    )

    t3 = BashOperator(
        task_id="load_into_database",
        bash_command="python /opt/airflow/scripts/load_into_database.py",
    )
    t3.doc_md = textwrap.dedent(
        """
        #### Task Documentation
        This is a task to load the validated banking data into the database using the `load_into_database.py` script.
        """
    )

    t4 = BashOperator(
        task_id="build_dbt_models",
        bash_command="""
        dbt build \
        --project-dir /opt/airflow/dbt \
        --profiles-dir /opt/airflow/dbt
        """
    )
    t4.doc_md = textwrap.dedent(
        """
        #### Task Documentation
        This is a task to build the dbt models using the `dbt build` command in the `/opt/airflow/dbt` directory.
        """
    )

    t1 >> t2 >> t3 >> t4