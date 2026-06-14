with

products as (

    select * from {{ ref('stg_baci_product_codes') }}
),

final as (
    select
        hs6_product_code,
        product_description
    from products
)

select * from final