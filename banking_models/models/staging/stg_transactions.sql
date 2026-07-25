{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['transaction_id', 'as_of_date']
) }}

select
    transaction_id,
    customer_id,
    transaction_date,
    amount,
    currency,
    transaction_type,
    status,
    branch_code,
    description,
    cast(transaction_date as date) as as_of_date
from {{ source('banking_raw', 'transactions_raw') }}