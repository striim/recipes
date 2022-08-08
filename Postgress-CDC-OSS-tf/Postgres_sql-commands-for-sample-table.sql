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

-- The below sql command creates a new role with replication permissions
CREATE ROLE replication_user NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN REPLICATION NOBYPASSRLS PASSWORD '<your-password>';


SELECT pg_create_logical_replication_slot('test_slot', 'wal2json');

