from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="paypal_payments_pipeline",
    default_args=DEFAULT_ARGS,
    description="End-to-end PayPal payments ingestion and analytics pipeline",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["paypal", "payments", "data-pipeline"],
) as dag:

    # 1️⃣ Fetch PayPal Orders
    fetch_orders = BashOperator(
        task_id="fetch_paypal_orders",
        bash_command="python3 /opt/airflow/project/scripts/fetch_payments.py",
    )

    # 2️⃣ Upload Raw Data to S3
    upload_raw_to_s3 = BashOperator(
        task_id="upload_raw_to_s3",
        bash_command="python3 /opt/airflow/project/scripts/upload_raw_to_s3.py",
    )

    # 3️⃣ Transform Orders → Payments Fact
    transform_orders = BashOperator(
        task_id="transform_orders_to_payments",
        bash_command="python3 /opt/airflow/project/transforms/transform_orders_to_payments.py",
    )

    # 4️⃣ Upload Processed Data to S3
    upload_processed_to_s3 = BashOperator(
        task_id="upload_processed_to_s3",
        bash_command="python3 /opt/airflow/project/scripts/upload_processed_to_s3.py",
    )

    # DAG Order
    fetch_orders >> upload_raw_to_s3 >> transform_orders >> upload_processed_to_s3