select
TO_INT(data[2]) as po_box,
TO_STRING(data[3]) as street_name,
TO_STRING(data[4]) as city,
TO_STRING(data[5]) as state,
TO_INT(data[6]) as zip,
TO_INT(data[7]) as customer_account_number,
TO_INT(data[8]) as order_id,
TO_STRING(data[9]) as sku,
TO_INT(data[10]) as order_amount,
TO_STRING(data[11]) as order_date
from l1_stream l
