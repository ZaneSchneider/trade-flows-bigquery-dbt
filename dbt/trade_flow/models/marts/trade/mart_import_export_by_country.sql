with

country_product_year as (
    select * from {{ ref('mart_import_export_by_product_country') }}
),

country_names as (
    select iso3, any_value(country_name) as country_name
    from {{ ref('dim_country') }}
    group by iso3
),

rolled as (
    select
        iso3,
        year,
        coalesce(sum(export_value_thousands_usd), 0) as export_value_thousands_usd,
        coalesce(sum(import_value_thousands_usd), 0) as import_value_thousands_usd
    from country_product_year
    group by iso3, year
),

final as (
    select
        rolled.iso3,
        rolled.year,
        country_names.country_name,
        rolled.export_value_thousands_usd,
        rolled.import_value_thousands_usd,
        rolled.export_value_thousands_usd - rolled.import_value_thousands_usd as trade_balance_thousands_usd
    from rolled
    left join country_names
        on rolled.iso3 = country_names.iso3
)

select * from final