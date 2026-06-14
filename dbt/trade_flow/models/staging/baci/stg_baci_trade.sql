with 

source as (
    select * from {{ source('trade_flow_v2_raw', 'baci_trade') }}
),

renamed as (
    select
        t as year,
        i as exporter_country_code,
        j as importer_country_code,
        k as hs6_product_code,
        v as trade_value_thousands_usd,
        q as trade_quantity_metric_tons
    from source
)

select * from renamed