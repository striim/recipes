select TO_STRING(data.get("ordertime")) as ordertime,
	   TO_STRING(data.get("orderid")) as orderid,
	   TO_STRING(data.get("itemid")) as itemid,
	   TO_STRING(data.get("address")) as address
from kafkaOutputStream;