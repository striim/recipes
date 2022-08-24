## Spark pool

from pyspark.sql.types import StructType, IntegerType, StringType

schema = StructType() \
      .add("lpo_box",StringType(),True) \
      .add("lstreet_name",StringType(),True) \
      .add("lcity",StringType(),True) \
      .add("lstate",StringType(),True) \
      .add("lzip",IntegerType(),True) \
      .add("lcustomer_account_number",IntegerType(),True) \
      .add("lorder_id",IntegerType(),True) \
      .add("lsku",StringType(),True) \
      .add("lorder_amount",IntegerType(),True) \
      .add("lorder_date",StringType(),True) \
      .add("ofirst_name",StringType(),True) \
      .add("olast_name",StringType(),True)


df = spark.read.format("csv") \
      .option("header", False) \
      .schema(schema) \
      .load("abfss://adls*******@******.dfs.core.windows.net/****")

df.printSchema()
display(df_with_schema.limit(10))


spark.sql("CREATE DATABASE IF NOT EXISTS retailordersdb")
df.repartition(1)
df.write.mode("overwrite").saveAsTable("retailordersdb.orders")
spark.sql("Select count(*) from retailordersdb.orders")

#spark.sql("drop table retailorders.ordercountstats  ")

df = spark.sql("""
   SELECT
        SUM(lorder_amount) as TotalOrderByState
   FROM retailordersdb.orders
   WHERE lorder_amount > 0
   GROUP BY lcity, lstate
""")
display(df)
df.write.saveAsTable("retailorders.ordercountsums")
