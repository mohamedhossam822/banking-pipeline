with txns as (
    select
        customer_id,
        currency,
        as_of_date,
        case
            when transaction_type in ('INTEREST','CREDIT') then amount
            when transaction_type in ('TRANSFER','DEBIT','FEE') then -amount
        end as signed_amount
    from {{ ref('stg_transactions') }}
    where status = 'COMPLETED'
),
daily as (
    select
        customer_id,
        currency,
        as_of_date,
        sum(signed_amount) as daily_net
    from txns
    group by customer_id, currency, as_of_date
)
select
    customer_id,
    currency,
    as_of_date,
    sum(daily_net) over (
        partition by customer_id, currency
        order by as_of_date
        rows between unbounded preceding and current row
    ) as running_balance
from daily