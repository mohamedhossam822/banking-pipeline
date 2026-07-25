WITH CTE AS (
SELECT customer_id,currency,
 CASE 
	WHEN transaction_type IN  ('INTEREST','CREDIT') THEN amount
	WHEN transaction_type IN  ('TRANSFER','DEBIT','FEE') THEN -amount

END AS daily_net ,
as_of_date
FROM {{ ref('stg_transactions') }}
)
SELECT customer_id,currency,as_of_date,sum(daily_net) over(partition by customer_id,currency order by (as_of_date)) 
from CTE