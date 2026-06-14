FROM python:3.12-slim

WORKDIR /

RUN pip install --no-cache-dir dbt-bigquery==1.11.1

# project + the container profile
COPY trade_flow /dbt/trade_flow
COPY profiles_docker.yml /dbt_profiles/profiles.yml

# install dbt_utils at build time so `dbt build` has it
RUN dbt deps --project-dir /dbt/trade_flow

CMD ["dbt", "build", "--project-dir", "/dbt/trade_flow", "--profiles-dir", "/dbt_profiles"]