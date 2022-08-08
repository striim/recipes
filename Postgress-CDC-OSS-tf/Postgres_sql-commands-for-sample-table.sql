create schema qatest;

create TABLE qatest.retaildata_cdc (
	STORE_ID varchar(50) not NULL,
	"NAME" varchar(50) NULL,
	CITY varchar(50) NULL,
	STATE varchar(50) NULL,
	ZIP varchar(50) NULL,
	CUSTOMER_ACCOUNT_NO varchar(50) NULL,
	ORDER_ID varchar(50) NULL,
	SKU varchar(50) NULL,
	ORDER_AMOUNT varchar(50) NULL,
	DATETIME varchar(50) NULL
);


SELECT pg_create_logical_replication_slot('test_slot', 'wal2json');


INSERT INTO qatest.retaildata_cdc
(store_id, "NAME", city, state, zip, customer_account_no, order_id, sku, order_amount, datetime)
VALUES('100', 'John Doe', 'Chicago', 'Illinois', '60007', '1234567', '98765', '1234567/S', '20', '20130801080012');

INSERT INTO qatest.retaildata_cdc
(store_id, "NAME", city, state, zip, customer_account_no, order_id, sku, order_amount, datetime)
VALUES('101', 'Jane Doe', 'Chicago', 'Illinois', '60007', '1234568', '98766', '1234567/E', '25', '20140801080012');
