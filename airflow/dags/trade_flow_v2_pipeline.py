import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime


HOST_SECRETS_DIR = os.environ["HOST_SECRETS_DIR"]

CREDENTIALS_MOUNT = Mount(
    source=HOST_SECRETS_DIR,
    target="/credentials",
    type="bind",
    read_only=True,
)

GCP_ENV = {
    "GOOGLE_APPLICATION_CREDENTIALS": "/credentials/baci-fetcher-key.json",
}

COMMON = dict(
    environment=GCP_ENV,
    mounts=[CREDENTIALS_MOUNT],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mount_tmp_dir=False,
)

with DAG(
    dag_id="trade_flow_v2_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["trade-flow", "v2"],
    doc_md="BACI → GCS → BigQuery → dbt build. Trigger manually on a new BACI version.",
) as dag:

    download_baci = DockerOperator(
        task_id="download_baci",
        image="baci-fetcher:latest",
        command="python fetch_baci.py",
        doc_md="Download BACI HS92, filter to wanted years, upload CSVs to GCS.",
        **COMMON,
    )

    load_baci = DockerOperator(
        task_id="load_baci_to_bigquery",
        image="baci-fetcher:latest",
        command="python load_to_bigquery.py",
        doc_md="Load BACI CSVs from GCS into the trade_flow_v2_raw dataset.",
        **COMMON,
    )

    dbt_build = DockerOperator(
        task_id="dbt_build",
        image="dbt-runner:latest",
        command="dbt build --project-dir /dbt/trade_flow --profiles-dir /dbt_profiles",
        doc_md="Seeds, models, and tests in dependency order.",
        **COMMON,
    )

    download_baci >> load_baci >> dbt_build