with 

source as (
    select * from {{ source('trade_flow_v2_raw', 'baci_country_codes') }}
),

renamed as (
    select
        country_code,
        -- fix encoding that corrupts certain names
        regexp_replace(
            safe_convert_bytes_to_string(code_points_to_bytes(to_code_points(country_name))),
            r'\s*\(\.\.\.\d{4}\)\s*$', ''
        ) as country_name, 
        country_iso2 as iso2,
        country_iso3 as iso3
    from source
)

select * from renamed