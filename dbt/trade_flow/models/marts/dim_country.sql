with 

country as (
    select * from {{ ref('stg_baci_country_codes') }}
),

final as (
    select
        country_code,
        country_name,
        iso2,
        iso3
    from country
)

select * from final