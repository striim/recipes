CREATE TABLE [dbo].[retail_data_pii]
(
    [lcustomer_account_number] int NOT NULL,
    [ofirst_name] varchar(50)  NULL,
    [olast_name] varchar(50)  NULL,
    [lpo_box] varchar(50)  NULL,
    [lstreet_name] varchar(50)  NULL,
    [lcity] varchar(50)  NULL,
    [lstate] varchar(50)  NULL,
    [lzip] int NULL,
    [lorder_id] int NULL,
    [lsku] varchar(50) NULL,
    [lorder_amount] int NULL,
    [lorder_date] varchar(50) NULL
)
WITH
(
    DISTRIBUTION = ROUND_ROBIN,
    CLUSTERED COLUMNSTORE INDEX
)
GO
