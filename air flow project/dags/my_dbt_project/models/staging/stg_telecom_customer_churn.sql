-- this model define the staging table doesn't store data 
{{ config(materialized='ephemeral') }}

WITH source_data AS (
    SELECT * FROM {{ source('raw_telecom', 'telecom_customer_churn') }}
)
-- Clean the data: rename columns 
SELECT
    "Gender" as gender,
    "Age" as age,
    "Married" as married,
    "Number of Dependents" as number_of_dependents,
    "Phone Service" as phone_service,
    "Multiple Lines" as multiple_lines,
    "Internet Service" as internet_service,
    "Internet Type" as internet_type,  
    "Online Security" as online_security,
    "Online Backup" as online_backup,
    "Device Protection Plan" as device_protection_plan, 
    "Premium Tech Support" as premium_tech_support, 
    "Streaming TV" as streaming_tv,
    "Streaming Movies" as streaming_movies,
    "Contract" as contract,
    "Paperless Billing" as paperless_billing,
    "Payment Method" as payment_method,
    "Monthly Charge" as monthly_charge,
    "Total Charges" as total_charges,
    "Customer Status" as customer_status
FROM source_data