import mysql.connector as sql
import tkinter
from tkinter import messagebox

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'textapp'
    )

def pop(action,message):
    root = tkinter.Tk()
    root.withdraw()
    if action == 'error':
        messagebox.showerror('Error',message)
    elif action == 'info':
        messagebox.showinfo('Info',message)
    root.destroy()

def add(action,username,password):

    cursor = db.cursor()
    if action == 'register':
        try:
            cursor.execute('SELECT id from details')
            count = cursor.fetchall()
            cursor.execute('''
            INSERT INTO details(id,username,password) VALUES(%s,%s,%s)''',(count[0][0]+1,username, password))

        except sql.IntegrityError:
            pop('error',"Username '" + username + "' already exists.")
        else:
            db.commit()  
        


    elif action == 'login':
        try:
            cursor.execute("""SELECT * from details where username = %s""",(username,)) #no curly brackets around %s, ensure tuple format.
            data = cursor.fetchall()
            if data[0][2] == password: #TYPE ERROR INCORRECT USEER.
                pop('info',"LOGIN SUCCESSFUL!")
            else:
                pop('error',"Incorrect Password")
        except: #index error since even if username doesn't exist in db, it gives empty tuple.
            pop('error',"User doesn't exist. Please try again.")  
        

    



    
    


