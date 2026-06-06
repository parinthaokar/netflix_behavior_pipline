from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

# 1. Point to your specific dbt directory inside include
DBT_PROJECT_PATH = Path("/usr/local/airflow/include/netflix_behavior_pipline")

default_args = {
    'owner': 'analytics_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    's3_to_snowflake_pipeline',
    default_args=default_args,
    description='automate loading data from s3 into snowflake and running dbt',
    schedule=None,
    catchup=False,
) as dag:
    
    # Fixed the spaces around the equals sign that was throwing your terminal error
    load_raw_data = SQLExecuteQueryOperator(
        task_id='copy_s3_to_snowflake',
        conn_id='snowflake_conn',
        sql="""
            COPY INTO NETFLIX_BEHAVIOR.RAW_DATA.USER_WATCHING_BEHAVIOR
            FROM @NETFLIX_BEHAVIOR.RAW_DATA.NETFLIX_RAW_DATA
            FILE_FORMAT = (FORMAT_NAME = 'NETFLIX_BEHAVIOR.PUBLIC.NETFLIX_CSV_FORMAT')
            ON_ERROR = 'CONTINUE';
        """
    )

    # 2. Configured exactly to map your Snowflake target database structure
    dbt_transform = DbtTaskGroup(
        group_id="dbt_transformations",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=ProfileConfig(
            profile_name="dbt_netflix",  # Matches your Snowflake schema folder name
            target_name="dev",
            profile_mapping=SnowflakeUserPasswordProfileMapping(
                conn_id="snowflake_conn",
                profile_args={
                    "database": "NETFLIX_BEHAVIOR",
                    "schema": "DBT_NETFLIX", 
                },
            ),
        ),
    )

    load_raw_data >> dbt_transform