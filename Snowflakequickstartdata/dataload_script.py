import numpy as np
import oracledb
import pandas as pd


def import_csv(filename):
    return pd.read_csv(filename, index_col=False).replace(np.nan, '', regex=True)


def connectAndSendData(username, password, db_url, file):
    connection = oracledb.connect(user=username, password=password, dsn=db_url)
    imported_data = import_csv(file)
    print("Connected to DB successfully")
    print("CSV conformed data into Pandas DF -> \n", imported_data)
    cursor = connection.cursor()
    print("Inserting CSV data into Oracle DB")
    imported_data["COMPLICATION_ID"] = pd.to_numeric(imported_data["COMPLICATION_ID"])
    imported_data["MEASURE_START_DT"] = pd.to_datetime(imported_data["MEASURE_START_DT"])
    imported_data["MEASURE_END_DT"] = pd.to_datetime(imported_data["MEASURE_END_DT"])
    counter = 0
    for index, row in imported_data.iterrows():
        sql_cmd = "INSERT INTO  " \
                  "HOSPITAL_COMPLICATIONS(COMPLICATION_ID,PROVIDER_ID,HOSPITAL_NAME, " \
                  "ADDRESS, CITY, STATE, ZIP_CODE, COUNTY, PHONE_NUMBER, MEASURE_NAME, MEASURE_ID, " \
                  "COMPARED_TO_NATIONAL, DENOMINATOR, SCORE, LOWER_ESTIMATE, " \
                  "HIGHER_ESTIMATE, FOOTNOTE, MEASURE_START_DT, MEASURE_END_DT) " \
                  "VALUES(:0,:1,:2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18)"
        cursor.execute(sql_cmd, tuple(row))
        counter += 1
        if counter == 5:
            connection.commit()
            counter = 0
    connection.commit()
    connection.close()
    print("done!")




if __name__ == "__main__":
    connectAndSendData(username="<your username>", password="<your password>", db_url="//<oracle hostname>:1521/<SID>",
                       file="HOSPITAL_COMPLICATIONS_202308291244.csv")

