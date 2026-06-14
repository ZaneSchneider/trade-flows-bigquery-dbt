
-- each partition currently < 0.5 GB
{{ config(
    partition_by={'field': 'year', 'data_type': 'int64',
                  'range': {'start': 1990, 'end': 2050, 'interval': 1}},
    cluster_by=['exporter_iso3', 'importer_iso3', 'hs6_product_code']
) }}

with

stg_baci as (
    select * from {{ ref('stg_baci_trade') }}
),

dim_country as (
    select * from {{ ref('dim_country') }}
),

final as (
    select
        stg_baci.year,
        a.iso3 as exporter_iso3,
        b.iso3 as importer_iso3,
        stg_baci.hs6_product_code,
        stg_baci.trade_value_thousands_usd,
        stg_baci.trade_quantity_metric_tons
    from stg_baci
    left join dim_country a 
        on stg_baci.exporter_country_code = a.country_code
    left join dim_country b 
        on stg_baci.importer_country_code = b.country_code
)

select * from final

