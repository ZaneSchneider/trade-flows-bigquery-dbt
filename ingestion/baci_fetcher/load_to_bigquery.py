from google.cloud import bigquery

PROJECT_ID = "trade-flow-analysis"
DATASET_ID = "trade_flow_v2_raw"
BUCKET = "trade-flow-analysis-raw"
PREFIX = "baci"

YEAR_URI = f"gs://{BUCKET}/{PREFIX}/BACI_HS92_Y*_V202601.csv"  # wildcard: all 30 years, one job
PRODUCT_CODES_URI = f"gs://{BUCKET}/{PREFIX}/product_codes_HS92_V202601.csv"
COUNTRY_CODES_URI = f"gs://{BUCKET}/{PREFIX}/country_codes_V202601.csv"

BACI_TRADE_SCHEMA = [
    bigquery.SchemaField("t", "INTEGER"),  # year
    bigquery.SchemaField("i", "INTEGER"),  # exporter (country_code)
    bigquery.SchemaField("j", "INTEGER"),  # importer (country_code)
    bigquery.SchemaField("k", "STRING"),   # HS6 product code (leading zeros)
    bigquery.SchemaField("v", "FLOAT"),    # value, thousands USD
    bigquery.SchemaField("q", "FLOAT"),    # quantity, metric tons 
]

PRODUCT_CODES_SCHEMA = [
    bigquery.SchemaField("code", "STRING"),
    bigquery.SchemaField("description", "STRING"),
]

COUNTRY_CODES_SCHEMA = [
    bigquery.SchemaField("country_code", "INTEGER"),
    bigquery.SchemaField("country_name", "STRING"),
    bigquery.SchemaField("country_iso2", "STRING"),
    bigquery.SchemaField("country_iso3", "STRING"),
]


def load_csv_to_bq(client, source_uri, table_id, schema):
    """Load CSV(s) from a GCS URI into a BigQuery table, replacing existing data.

    Adapted from:
    https://github.com/googleapis/python-bigquery/blob/main/samples/load_table_uri_csv.py
    """
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # idempotent reruns
    )
    load_job = client.load_table_from_uri(source_uri, table_id, job_config=job_config)
    load_job.result()  # wait for completion
    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}")


def table_id(name):
    return f"{PROJECT_ID}.{DATASET_ID}.{name}"


def main():
    client = bigquery.Client(project=PROJECT_ID)
    load_csv_to_bq(client, YEAR_URI, table_id("baci_trade"), BACI_TRADE_SCHEMA)
    load_csv_to_bq(client, PRODUCT_CODES_URI, table_id("baci_product_codes"), PRODUCT_CODES_SCHEMA)
    load_csv_to_bq(client, COUNTRY_CODES_URI, table_id("baci_country_codes"), COUNTRY_CODES_SCHEMA)


if __name__ == "__main__":
    main()