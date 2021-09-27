

import mysql.connector as sql

def createDB(dbname):
    db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
    )
    cursor = db.cursor(buffered=True)
    cursor.execute('''CREATE DATABASE IF NOT EXISTS {dbname}'''.format(dbname = dbname))


createDB('users_db')

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'users_db'
    )

def createDetails():
    cursor = db.cursor()
    cursor.execute('''Create table if not exists details
    (
        id int primary key,
        username varchar(50),
        password varchar(50)
    )''')

createDetails()



#function to register/login and fetch data from sqldb
def add(action,username,password,session):
    cursor = db.cursor()
    
    if action == 'register':
        try:
            if ' ' in username:
                return ("No spaces are allowed in the username.")
            cursor.execute('SELECT id from details')
            count = cursor.fetchall()
            #if no user is registered, count is [], else [(0,), (1,), (2,) ...]
            if len(count) == 0:
                count.append((0,))
            cursor.execute('''
            INSERT INTO details(id,username,password) VALUES(%s,%s,%s)''',(count[-1][0]+1,username, password))
    
        except sql.IntegrityError:
            return("Username '" + username + "' already exists.")
        else:
            db.commit()  
            return("User '" + username + "' registered successfully!")

    elif action == 'login':
        try:
            cursor.execute("""SELECT * from details where username = %s""",(username,)) #no curly brackets around %s, ensure tuple format.
            data = cursor.fetchall()
            #check if password matches that of the username, and no user currently logged in.
            if data[0][2] == password and session.get('username') is None: 
                return("Login successful!")
            #password maybe right, but some user is already logged in.
            elif session.get('username') is not None:
                return("A user is already logged in. Please logout first to login.")
            else:
                return("Incorrect password. Please try again.")
        except: 
            return("User doesn't exist. Please try again.")     
        
        
    



    
    


