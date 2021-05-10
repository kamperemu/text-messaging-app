import mysql.connector as sql

db = sql.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'root',
        database = 'textapp'
    )

def add(action,username,password):

    cursor = db.cursor()
    if action == 'register':
        try:
            cursor.execute('''
            INSERT INTO details(username,password) VALUES(%s,%s)''',(username, password))

        except sql.IntegrityError:
            print("Username '",username,"' already exists.")
        except:
            print("Invalid Data.")
        else:
            db.commit()  
        


    elif action == 'login':
        try:
            cursor.execute("""SELECT * from details where username = %s""",(username,)) #no curly brackets around %s, ensure tuple format.
            data = cursor.fetchone()
            if data[2] == password: #TYPE ERROR INCORRECT USEER.
                print("LOGIN SUCCESSFUL!")
            else:
                print("Incorrect Password")
        except: #index error since even if username doesn't exist in db, it gives empty tuple.
            print("User doesn't exist. Please try again.")  
        

    



    
    


