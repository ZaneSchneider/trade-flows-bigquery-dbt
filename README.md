# Global Trade Flow ELT Pipeline

End-to-end data pipeline that turns 30 years of raw bilateral trade records into a
tested, queryable model of world trade.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trade-flows-bigquery-dbt.streamlit.app/)

[![dbt CI](https://github.com/ZaneSchneider/trade-flows-bigquery-dbt/actions/workflows/ci.yml/badge.svg)](https://github.com/ZaneSchneider/trade-flows-bigquery-dbt/actions/workflows/ci.yml)

```mermaid
flowchart LR
  src["BACI HS92 panel<br/>CEPII · 1995–2024"]
  gcs[("Cloud Storage<br/>raw files")]
  bq[("BigQuery<br/>raw")]
  stg["dbt staging<br/>(views)"]
  marts["dbt marts (tables)<br/>dim_country · dim_product · fct_trade<br/>+ analytical marts"]
  dash["Streamlit dashboards"]

  src -->|Docker fetcher| gcs --> bq --> stg --> marts --> dash
  air(["Airflow"]) -. orchestrates .-> gcs
  air -. orchestrates .-> marts
  tf(["Terraform · IaC"]) -. provisions .-> gcs
  tf -. provisions .-> bq
  ci(["GitHub Actions CI<br/>keyless OIDC · tests PRs"]) -. validates .-> marts
```

## Overview

Models global merchandise trade (1995–2024) so that questions like *what does the world
trade most, which countries run the largest surpluses and deficits, and in which
commodities* can be answered against governed, tested marts instead of a raw
~270M-row table. Built to own every stage: ingestion, warehousing, transformation,
testing, orchestration, and a dashboard layer.

## Data

[BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) (CEPII) —
the cleaned, reconciled version of UN Comtrade bilateral trade flows (release V202601).

- Grain: exporter × importer × product (HS6) × year
- Coverage: 1995–2024 (~270M flow records)
- Units: value in thousands USD; quantity in metric tons (partial)

## Stack

| Stage | Tool |
|---|---|
| Ingestion | Python fetcher in Docker → Google Cloud Storage |
| Warehouse | Google BigQuery |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| Infrastructure | Terraform |
| Dashboards | Streamlit |
| CI/CD | GitHub Actions (keyless OIDC → BigQuery) |

## Data modeling

dbt is layered **staging → marts**. Staging is one cleaned view per source (light
renames and typing); marts are materialized tables holding conformed dimensions
(`dim_country`, `dim_product`), the bilateral fact (`fct_trade`), and analytical
marts rolled up from it.

| Mart | Grain |
|---|---|
| `mart_trade_by_country_product` | country × product × year |
| `mart_trade_by_country` | country × year |
| `mart_trade_by_product` | product × year |

Data quality is enforced with dbt tests — `not_null`, `relationships`,
`accepted_range`, and `unique_combination_of_columns` on each model's declared grain.
Messy real-world issues are resolved in-model: reversing UTF-8 mojibake in country
names, and keying the trade fact on BACI's numeric `country_code` (the dimension's
true unique key) rather than `iso3`, which is non-unique because historical entities
share an ISO3 with their modern successor — Belgium-Luxembourg with Belgium (`BEL`),
the former Federal Republic of Germany with Germany (`DEU`), and the pre-2011 and
current Republic of Sudan (both `SDN`, both even labelled "Sudan"). ISO3 is carried
as a descriptive attribute and resolved through `dim_country`, so the fact's grain
stays honest and joins can't fan out.

## Dashboards

Streamlit app; all aggregation lives in SQL against the marts, so the pages only set
controls and render.

- **Country Trade Balance** — a country's largest trade surpluses and deficits
- **Commodity Trade Balance** — a country's commodities ranked by net balance
- **Top Traded Products** — most-traded commodities worldwide, with trend over time

Open in Streamlit: [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trade-flows-bigquery-dbt.streamlit.app/)

## Continuous integration

Every pull request to `main` runs a GitHub Actions workflow that builds and tests the
dbt project against BigQuery, so broken changes can't merge. The runner authenticates
to Google Cloud with **no long-lived key**: GitHub issues a short-lived OIDC token,
Workload Identity Federation exchanges it for temporary credentials scoped to this
repository, and a least-privilege service account (`bigquery.jobUser` +
`bigquery.dataEditor`) runs the build.

To keep CI fast and nearly free, models are built with `dbt run --empty` (zero rows) —
enough to validate that the project compiles, every `ref`/`source` resolves, and every
model contract holds — and unit tests then run on mocked inputs. The CI build is
isolated in its own `dbt_ci` dataset.

## Roadmap

- Quantities and unit values (price per metric ton)
- Price-penalty analysis — where exporters sell the same commodity for systematically less

## Notes

Raw data lives in Cloud Storage, not in this repo. Credentials (service-account key,
dbt profiles) are gitignored and never committed.

## Attribution

Trade data © CEPII (BACI), used under CEPII's terms. Code is released under the [MIT License](LICENSE).