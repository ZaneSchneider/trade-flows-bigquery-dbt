with 

source as (
    select * from {{ source('trade_flow_v2_raw', 'baci_product_codes') }}
),

renamed as (
    select
        code as hs6_product_code,
        description as product_description
    from source
)

select * from renamed