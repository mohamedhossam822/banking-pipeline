select
    customer_id,
    full_name,
    email,
    phone,
    country,
    account_type,
    credit_score,
    is_active,
    dbt_valid_from,
    dbt_valid_to
from {{ ref('customers_snapshot') }}
--where dbt_valid_to is null