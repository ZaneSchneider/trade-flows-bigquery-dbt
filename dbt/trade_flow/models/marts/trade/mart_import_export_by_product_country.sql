

with

fct_trade as (
    select * from {{ ref('fct_trade') }}
),

exports as (
    select
        exporter_iso3 as iso3,
        hs6_product_code,
        year,
        sum(trade_value_thousands_usd) as export_value_thousands_usd,
        sum(trade_quantity_metric_tons) as export_quantity_metric_tons
    from fct_trade
    group by 1, 2, 3
),

imports as (
    select
        importer_iso3 as iso3,
        hs6_product_code,
        year,
        sum(trade_value_thousands_usd) as import_value_thousands_usd,
        sum(trade_quantity_metric_tons) as import_quantity_metric_tons
    from fct_trade
    group by 1, 2, 3
),

final as (
    select
        coalesce(exports.iso3, imports.iso3) as iso3,
        coalesce(exports.hs6_product_code, imports.hs6_product_code) as hs6_product_code,
        coalesce(exports.year, imports.year) as year,
        exports.export_value_thousands_usd,
        exports.export_quantity_metric_tons,
        imports.import_value_thousands_usd,
        imports.import_quantity_metric_tons
    from exports
    full outer join imports 
        on exports.iso3 = imports.iso3 
        and exports.hs6_product_code = imports.hs6_product_code 
        and exports.year = imports.year
)

select * from final