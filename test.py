import pymysql
import creds

try:
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        port=3306
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
