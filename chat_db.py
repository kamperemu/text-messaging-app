import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

def createTable(host,roomID):
    cursor = db.cursor()
    cursor.execute(''' SHOW TABLES LIKE 't_{host}' '''.format(host = host))
    checkTable = cursor.fetchone()
    if checkTable is not None:
        cursor.execute("TRUNCATE TABLE t_{host} ".format(host=host))
    cursor.execute('''CREATE TABLE IF NOT EXISTS t_{host}
     (roomID varchar(10) default 'None',
      users varchar(50) default  'None',
      message varchar(150) default 'None')'''.format(host = host))
    #Unknown column error, hence put '' around id,host in values (else not treated as a string.)
    cursor.execute('''INSERT INTO t_{host}(roomID, users) values ('{id}','{host}')'''.format(host = host, id = roomID))
    db.commit()
    
def connect(curUser,host,roomID):
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
            cursor.execute("INSERT INTO t_{host}(users) VALUES ('{user}')".format(host = host, user = curUser))
            return "Successfully connected to the chatroom!"
        else:
            return "One or more details are incorrectly entered."

def joinedUsers(host):
    cursor = db.cursor()
    cursor.execute("SELECT users from t_{host}".format(host = host))
    data = cursor.fetchall()
    return data




    