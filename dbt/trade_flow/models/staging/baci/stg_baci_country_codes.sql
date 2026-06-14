with 

source as (
    select * from {{ source('trade_flow_v2_raw', 'baci_country_codes') }}
),

renamed as (
    select
        country_code,
        country_name,
        country_iso2 as iso2,
        country_iso3 as iso3
    from source
)

select * from renamed