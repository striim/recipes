from datetime import datetime
import mysql.connector
from faker import Faker

num_partitions = 250000

# connect to mysql db, create cursor, setup sql command
connectmysql = mysql.connector.connect(
    host="<your hostname>",
    user="<user>",
    password="<password>",
    database="<Database>"
)
sqlcursor = connectmysql.cursor()
print(connectmysql)
sql = "INSERT INTO Retail.cctxn (cc_number, amount, txn_type, session_id, txn_timestamp) VALUES(%s,%s,%s,%s, CURRENT_TIMESTAMP)"

#fake data from faker
fake = Faker()
cc_number = [fake.unique.credit_card_number() for i in range(num_partitions)]
if (cc_number):
    print("Successfully created", len(cc_number), "unique credit card numbers")
session_id = [fake.unique.random_number(digits=len(str(num_partitions)), fix_len=True) for i in range(num_partitions)]
if (cc_number):
    print("Successfully created", len(cc_number), "unique session id numbers")

# batch insert function
def writeBatch(txn_type, start, end):
    events = []
    for i in range(start,end):
        event = (cc_number[i], fake.random_number(digits=5, fix_len=False), txn_type, session_id[i])
        events.append(event)
    sqlcursor.executemany(sql,events)
    connectmysql.commit()
    print(sqlcursor.rowcount, txn_type + " records were inserted as CDC.")

# 1M TXN - 250K Partition Set 
writeBatch("AUTH/HOLD", 0, 250000)
writeBatch("AUTH/HOLD", 0, 250000)
writeBatch("CHARGE", 240000,250000)
writeBatch("AUTH/HOLD", 0, 240000)
writeBatch("CHARGE", 220000,240000)
writeBatch("AUTH/HOLD", 0, 210000)
writeBatch("CHARGE", 200000,220000)


# # 4M TXN - 1M Partition Set
# writeBatch("AUTH/HOLD", 0, 1000000)
# writeBatch("AUTH/HOLD", 0, 1000000)
# writeBatch("CHARGE", 950000,1000000)
# writeBatch("AUTH/HOLD", 0, 900000)
# writeBatch("CHARGE", 850000,950000)
# writeBatch("AUTH/HOLD", 0, 850000)
# writeBatch("CHARGE", 750000,850000)

# close connection
sqlcursor.close()
connectmysql.close()