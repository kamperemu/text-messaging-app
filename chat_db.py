import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

def createTable(host,roomID):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS t_{name}
     (roomID varchar(10) default 'None',
      message varchar(150) default 'None')'''.format(name = host))
    cursor.execute('''INSERT INTO t_{name}(roomID) values ({id})'''.format(name = host, id = roomID))
    db.commit()
    
def connect(host, roomID):
    cursor = db.cursor()
    cursor.execute(''' SHOW TABLES LIKE 't_{host}' '''.format(host = host))
    hostname = cursor.fetchone()

    if hostname == None:
        return "This user has not hosted a room currently."
    else:
        hostname = hostname[0]
        cursor.execute(" SELECT roomID from t_{host} where roomID != 'None' ".format(host = host))
        checkID = cursor.fetchone()[0]

        if checkID == roomID and hostname[2::] == host:
            return "Successfully connected to the chatroom!"
        else:
            return "One or more details are incorrectly entered."



    