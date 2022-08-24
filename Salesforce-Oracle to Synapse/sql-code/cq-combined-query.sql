select
l.po_box,
l.street_name,
l.city,
l.state,
l.zip,
l.customer_account_number,
l.order_id,
l.sku,
l.order_amount,
l.order_date,
o.FIRST_NAME,
o.LAST_NAME
from L2_COMBINED l, oracle_db_cache o
where l.customer_account_number = o.CUSTOMER_ACCOUNT_NO
