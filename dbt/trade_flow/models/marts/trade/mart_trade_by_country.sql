with

country_product_year as (
    select * from {{ ref('mart_trade_by_country_product') }}
),

dim_country as (
    select * from {{ ref('dim_country') }}
),

rolled as (
    select
        country_code,
        year,
        coalesce(sum(export_value_thousands_usd), 0) as export_value_thousands_usd,
        coalesce(sum(import_value_thousands_usd), 0) as import_value_thousands_usd
    from country_product_year
    group by country_code, year
),

final as (
    select
        rolled.country_code,
        dim_country.iso3,
        dim_country.country_name,
        rolled.year,
        rolled.export_value_thousands_usd,
        rolled.import_value_thousands_usd,
        rolled.export_value_thousands_usd - rolled.import_value_thousands_usd as trade_balance_thousands_usd
    from rolled
    left join dim_country
        on rolled.country_code = dim_country.country_code
)

select * from final