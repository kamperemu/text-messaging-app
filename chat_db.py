import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

def createTable(host):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS t_{name} (message varchar(150) default 'None')".format(name = host))
    db.commit()
    