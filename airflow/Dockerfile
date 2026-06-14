FROM apache/airflow:2.9.0

USER root

RUN groupadd -g 975 docker_host || true \
    && usermod -aG docker_host airflow

USER airflow

RUN pip install --no-cache-dir apache-airflow-providers-docker