import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

def createTable(id):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS _%s (user varchar(50), message varchar(150))",(id,))
    db.commit()
