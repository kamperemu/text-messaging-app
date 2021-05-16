from flask import Flask, redirect, render_template, request, url_for, session
import mod_db as userdb
import socket
import time, random
import chat_db as roomdb

app = Flask(__name__)
app.secret_key = 'duosandounsaoudasuodousandos'

def add_data(action,username,password):
    if username != '' and password != '':
        return(userdb.add(action,username,password,session))


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form.get('logout'):
            #if no user logged in, can't perform the logout action.
            if 'username' not in session:
                return render_template('home.html', info = 'No user is currently logged in.')
            #if some user is logged in, remove it from the session.
            else:
                user = session.pop('username')
                session.pop('password')
                return render_template('home.html', info = "User '" + user + "' logged out successfully!")
    elif request.method == 'GET':        
        print(session)
        return render_template('home.html', info='')


@app.route("/register", methods = ["POST",'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #result is the returned output which tells us whether the user exists or not.
        result = add_data('register',username,password)
        return render_template('register.html', head = 'Registration!', pagetitle = 'Register', user_status = result)
    else:
        #before submitting the form, while in get method, result is not executed since no post has been done.
        return render_template('register.html', head = 'Registration!', pagetitle = 'Register', user_status = '')

def rand_id():
    return random.randint(10000000,99999999)

def roomTable():
    roomdb.createTable(session['username'])

#CREATE TABLE FOR CHAT

@app.route("/login", methods = ["POST",'GET'])
def login():
    #click the submit button on login page
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = add_data('login',username,password)
        #iff successful login and no other user logged in
        if result == "Login successful!" and session.get('username') is None:
            session['username'] = username
            session['password'] = password
            time.sleep(1)
            return redirect(url_for('chatroomIndex'))

        else:
            #unsuccessful login by:
            #1: no field empty but someone is logged in
            if result is not None and 'username' in session:
                return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = "A user is already logged in.")
            #2: no field empty but no user is logged in
            elif result is not None and 'username' not in session:
                print(session)
                return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = result)
            #3: some field empty, and a user is logged in 
            elif result is None and 'username' in session: 
                return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = "A user is already logged in.") 
            #4: one or more fields empty while no user is logged in.
            else:
                return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = "Invalid details. Please try again.")
                
    else:
        #just visiting the login page.
        return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = '')


#page where user chooses to join or create a room.
@app.route('/chatroom', methods = ["GET","POST"])
def chatroomIndex():
    if 'username' in session:
        if request.method == "POST":
            if request.form.get('create'):
                tableId = rand_id()
                roomTable()
                return redirect(url_for('roomFinal',id=tableId))

            elif request.form.get('join'):
                userEnteredId = request.form['userEnteredId']
                #MATCH USERENTEREDID WITH ANY EXISTING CHATROOM
                #MAKE USE OF RANDOM ID
                
        else:
            return render_template('chatroom_index.html')
    else:
        return render_template('home.html', info = "Log in first to join a chatroom.")

@app.route('/room/id=<id>', methods = ["GET","POST"])
def roomFinal(id):
    if 'username' in session:
        url = request.url
        id = url[-1:-9:-1][::-1]
        print(id)
        return render_template('roomFinal.html',id=id)
    else:
        return render_template('home.html', info = "Log in first to join a chatroom.")

#get local ip address of the server-host device.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(debug = True, host = ip_address, port = 5000)
