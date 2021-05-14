import mysql.connector as sql
import tkinter
from tkinter import messagebox

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'textapp'
    )


#function to register/login and fetch data from sqldb
def add(action,username,password,session):
    cursor = db.cursor()
    if action == 'register':
        try:
            cursor.execute('SELECT id from details')
            count = cursor.fetchall()
            cursor.execute('''
            INSERT INTO details(id,username,password) VALUES(%s,%s,%s)''',(count[0][0]+1,username, password))
    
        except sql.IntegrityError:
            return("Username '" + username + "' already exists.")
        else:
            db.commit()  
            return("User '" + username + "'registered successfully!")

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
            #entering a wrong username while a user is already logged in.
            if session.get('username') is None:
                return("A user is already logged in. Please logout first to login.")
            elif 'username' not in session or 'password' not in session:
                #entering empty username/password
                return("User doesn't exist. Please try again.")  
        
#EMPTY USERNAME LOGIN GIVING NONE.
    



    
    


