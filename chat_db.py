import mysql.connector as sql

def createDB(dbname):
    db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
    )
    cursor = db.cursor(buffered=True)
    cursor.execute('''CREATE DATABASE IF NOT EXISTS {dbname}'''.format(dbname = dbname))


createDB('chat_db')


db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'chat_db'
    )

#so each table represents a chat room. each unique chatroom has a unique host and a unique session id.
#named the table by the user's username for easier referencing
def createTable(host,roomID):
    lowerhost = host.lower()
    cursor = db.cursor()
    cursor.execute(''' SHOW TABLES LIKE 't_{host}' '''.format(host = lowerhost))
    checkTable = cursor.fetchone()
    if checkTable is not None:
        cursor.execute("TRUNCATE TABLE t_{host} ".format(host=lowerhost))
    cursor.execute('''CREATE TABLE IF NOT EXISTS t_{host}
     (roomID varchar(10) default 'None',
      users varchar(50) default 'None',
      message varchar(150) default 'None')'''.format(host = lowerhost))
    #Unknown column error, hence put '' around id,host in values (else not treated as a string.)
    cursor.execute('''INSERT INTO t_{host1}(roomID, users) values ('{id}','{host2}')'''.format(host1 = lowerhost, host2 = host, id = roomID))
    db.commit()
    

def connect(curUser,host,roomID, correctHost):
    cursor = db.cursor()
    lowerhost = host.lower()
    #get list of all tables to see if the host has already hosted one room or not
    cursor.execute(''' SHOW TABLES LIKE 't_{host}' '''.format(host = lowerhost))
    hostname = cursor.fetchone()

    #hostname field is left empty
    if hostname == None or host != correctHost:
        return "Invalid details entered"

    elif host == correctHost:
        hostname = hostname[0]
        cursor.execute(" SELECT roomID from t_{host} where roomID != 'None' ".format(host = lowerhost))
        checkID = cursor.fetchone()[0]

        #successfully connected to a room, insert the user's name in the table for the corresponding host.
        if checkID == roomID and hostname[2::] == lowerhost:
            cursor.execute("INSERT INTO t_{host}(users) VALUES ('{user}')".format(host = host, user = curUser))
            return "Successfully connected to the chatroom!"
        else:
            return "Invalid details entered"


#get list of all users in a room
def joinedUsers(host):

    lowerhost = host.lower()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT distinct users from t_{host}".format(host = lowerhost))
        data = cursor.fetchall()
        return data
    except:
        return "room ended"

#add the user along with the message he entered in the db
def appendMsg(user, msg, host):
    lowerhost = host.lower()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO t_{host}(users, message)
                    values ('{user}','{msg}')'''.format(host = lowerhost, user = user, msg = msg))
    db.commit()

#select all (users:message) from the database to display in the room.
def get_allMsg(host):
    lowerhost = host.lower()
    cursor = db.cursor()
    cursor.execute("SELECT users,message from t_{host} where message != 'None'".format(host = lowerhost))
    data = cursor.fetchall()
    return data

def endroom(host):
    lowerhost = host.lower()
    cursor = db.cursor()
    cursor.execute("DROP TABLE t_{host}".format(host = lowerhost))
    db.commit()