from faker import Faker
import datetime
import time
import csv

num_partitions = 250000

# create unique credit card numbers as unique partitions
fake = Faker()
cc_number = [fake.unique.credit_card_number() for i in range(num_partitions)]
if (cc_number):
    print("Successfully created", len(cc_number), "unique credit card numbers")
session_id = [fake.unique.random_number(digits=len(str(num_partitions)), fix_len=True) for i in range(num_partitions)]
if (cc_number):
    print("Successfully created", len(cc_number), "unique session id numbers")

# write event batches for given transaction type and partition indices
def writeBatch(txn_type, start, end):
    f = open("CC_TXN.csv", "a")
    writer = csv.writer(f)
    for i in range(start,end):
        event = [cc_number[i], fake.random_number(digits=5, fix_len=False), txn_type, session_id[i], datetime.datetime.now()]
        writer.writerow(event)
        time.sleep(0.0001)
    f.close()
    print("Successfully written", end - start, txn_type, "records into file")

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