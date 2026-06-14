with

products as (

    select * from {{ ref('stg_baci_product_codes') }}
),

hs_sections as (
    select * from {{ ref('hs_sections') }}
),

final as (
    select
        products.hs6_product_code,
        products.product_description,
        substr(products.hs6_product_code, 1, 2) as hs2,
        substr(products.hs6_product_code, 1, 4) as hs4,
        hs_sections.chapter_description,
        hs_sections.hs_section,
        hs_sections.section_description
    from products
    left join hs_sections 
        on substr(products.hs6_product_code, 1, 2) = lpad(cast(hs_sections.hs2 as string), 2, '0')
)

select * from final