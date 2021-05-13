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
def add(action,username,password):
    cursor = db.cursor()
    if action == 'register':
        try:
            cursor.execute('SELECT id from details')
            count = cursor.fetchall()
            print(count)
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
            if data[0][2] == password: 
                return("Login successful!")
            else:
                return("Incorrect Password")
        except: #index error since even if username doesn't exist in db, it gives empty tuple.
            return("User doesn't exist. Please try again.")  
        

    



    
    


