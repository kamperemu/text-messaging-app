import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

cursor = db.cursor()
cursor.execute('SHOW TABLES')
data = cursor.fetchall()
print(data)