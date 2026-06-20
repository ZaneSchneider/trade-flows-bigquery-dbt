{{ config(
    partition_by = {'field': 'year', 'data_type': 'int64',
                  'range': {'start': 1990, 'end': 2050, 'interval': 1}},
    cluster_by = ['exporter_country_code', 'importer_country_code', 'hs6_product_code']
) }}

with

stg_baci as (
    select * from {{ ref('stg_baci_trade') }}
),

final as (
    select
        year,
        exporter_country_code,
        importer_country_code,
        hs6_product_code,
        trade_value_thousands_usd,
        trade_quantity_metric_tons
    from stg_baci
)

select * from final

