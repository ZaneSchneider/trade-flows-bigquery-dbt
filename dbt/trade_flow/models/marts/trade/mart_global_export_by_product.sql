with

import_export_by_product_country as (
    select * from {{ ref('mart_import_export_by_product_country') }}
),

products as (
    select * from {{ ref('dim_product') }}
),

rolled as (
    select
        hs6_product_code,
        year,
        coalesce(sum(export_value_thousands_usd), 0) as trade_value_thousands_usd,
        sum(export_quantity_metric_tons) as trade_quantity_metric_tons
    from import_export_by_product_country
    group by hs6_product_code, year
),

final as (
    select
        rolled.hs6_product_code,
        rolled.year,
        products.product_description,
        rolled.trade_value_thousands_usd,
        rolled.trade_quantity_metric_tons
    from rolled
    left join products 
        on rolled.hs6_product_code = products.hs6_product_code
)

select * from final