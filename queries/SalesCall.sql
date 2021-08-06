SELECT
    customer_name AS name,
    customer_tel AS phone,
    customer_email AS email,
    gclid,
    campain,
    from_landing,
    created_at AS dt,
    shopify_order_id,
    (
        CASE
            WHEN shopify_order_id <> '0' THEN 'shopify_order'
            ELSE 'salescall'
        END
    ) AS source
FROM
    vuanem_ecommerce.vuanem_salescall_salescall vss
