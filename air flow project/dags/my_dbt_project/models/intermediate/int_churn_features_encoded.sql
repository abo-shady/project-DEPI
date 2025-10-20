-- models/intermediate/int_churn_features_encoded.sql
{{ config(materialized='table') }}

with source_data as (
    select * from {{ ref('int_customers_imputed') }}
),

encoded as (
    select
        age::int as age,
        number_of_dependents::int as dependents,
        monthly_charge::numeric as monthly_charge,
        total_charges::numeric as total_charges,

       
        case when lower(trim(gender)) = 'male' then 1 else 0 end as gender_encoded,
        case when lower(trim(married)) = 'yes' then 1 else 0 end as married_encoded,
        case when lower(trim(phone_service)) = 'yes' then 1 else 0 end as phone_service_encoded,
        case when lower(trim(multiple_lines)) = 'yes' then 1 else 0 end as multiple_lines_encoded,
        case when lower(trim(online_security)) = 'yes' then 1 else 0 end as online_security_encoded,
        case when lower(trim(online_backup)) = 'yes' then 1 else 0 end as online_backup_encoded,
        case when lower(trim(device_protection_plan)) = 'yes' then 1 else 0 end as device_protection_encoded,
        case when lower(trim(premium_tech_support)) = 'yes' then 1 else 0 end as tech_support_encoded,
        case when lower(trim(streaming_tv)) = 'yes' then 1 else 0 end as streaming_tv_encoded,
        case when lower(trim(streaming_movies)) = 'yes' then 1 else 0 end as streaming_movies_encoded,
        case when lower(trim(paperless_billing)) = 'yes' then 1 else 0 end as paperless_billing_encoded,
        case when lower(trim(internet_type)) = 'fiber optic' then 2
             when lower(trim(internet_type)) = 'dsl' then 1
             else 0 end as internet_service_encoded,
        case when lower(trim(contract)) = 'two year' then 2
             when lower(trim(contract)) = 'one year' then 1
             else 0 end as contract_encoded, 
        case when lower(trim(payment_method)) like '%credit card%' then 1
             when lower(trim(payment_method)) like '%bank withdrawal%' then 2
             when lower(trim(payment_method)) like '%mailed check%' then 3
             else 4 end as payment_method_encoded, 
        case when lower(trim(customer_status)) = 'churned' then 1
             else 0 end as churn_label

    from source_data
)

select * from encoded