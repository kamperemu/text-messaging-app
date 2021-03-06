import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'roomdb'
    )

#so each table represents a chat room. each unique chatroom has a unique host and a unique session id.
#named the table by the user's username for easier referencing
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
    #get list of all tables to see if the host has already hosted one room or not
    cursor.execute(''' SHOW TABLES LIKE 't_{host}' '''.format(host = host))
    hostname = cursor.fetchone()

    #hostname field is left empty
    if hostname == None:
        return "Invalid details entered"

    else:
        hostname = hostname[0]
        cursor.execute(" SELECT roomID from t_{host} where roomID != 'None' ".format(host = host))
        checkID = cursor.fetchone()[0]

        #successfully connected to a room, insert the user's name in the table for the corresponding host.
        if checkID == roomID and hostname[2::] == host:
            cursor.execute("INSERT INTO t_{host}(users) VALUES ('{user}')".format(host = host, user = curUser))
            return "Successfully connected to the chatroom!"
        else:
            return "Invalid details entered"


#get list of all users in a room
def joinedUsers(host):
    cursor = db.cursor()
    cursor.execute("SELECT distinct users from t_{host}".format(host = host))
    data = cursor.fetchall()
    return data

#add the user along with the message he entered in the db
def appendMsg(user, msg, host):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO t_{host}(users, message)
                    values ('{user}','{msg}')'''.format(host = host, user = user, msg = msg))
    db.commit()

#select all (users:message) from the database to display in the room.
def get_allMsg(host):
    cursor = db.cursor()
    cursor.execute("SELECT users,message from t_{host} where message != 'None'".format(host = host))
    data = cursor.fetchall()
    return data

    