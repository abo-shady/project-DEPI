-- models/intermediate/int_customers_imputed.sql
{{ config(materialized='ephemeral') }}

WITH source_data AS (
    SELECT * FROM {{ ref('stg_telecom_customer_churn') }}
),

stats AS (
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_charges) AS median_total_charges,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_charge) AS median_monthly_charge
    FROM source_data
    WHERE total_charges IS NOT NULL
)

SELECT
    source_data.gender,
    source_data.age,
    source_data.married,
    source_data.number_of_dependents,
    source_data.phone_service,
    source_data.multiple_lines,
    source_data.internet_service,
    source_data.internet_type,
    source_data.online_security,
    source_data.online_backup,
    source_data.device_protection_plan,
    source_data.premium_tech_support,
    source_data.streaming_tv,
    source_data.streaming_movies,
    source_data.contract,
    source_data.paperless_billing,
    source_data.payment_method,
    source_data.customer_status,

    COALESCE(source_data.total_charges, stats.median_total_charges) AS total_charges,
    COALESCE(source_data.monthly_charge, stats.median_monthly_charge) AS monthly_charge

FROM source_data
CROSS JOIN stats