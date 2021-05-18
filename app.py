from flask import Flask, redirect, render_template, request, url_for, session, flash
from bs4 import BeautifulSoup as Soup
import socket
import users_db as userdb
import time, random
import chat_db as roomdb


app = Flask(__name__)
app.secret_key = 'duosandounsaoudasuodousandos'




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
        return render_template('home.html', info='')

def add_data(action,username,password):
    if username != '' and password != '':
        return(userdb.add(action,username,password,session))

@app.route("/register", methods = ["POST",'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #result is the returned output which tells us whether the user exists or not.
        result = add_data('register',username,password)
        if result is None:
            return render_template('register.html', head = 'Registration!', pagetitle = 'Register', user_status = "Invalid details. Please try again.")
        return render_template('register.html', head = 'Registration!', pagetitle = 'Register', user_status = result)
    else:
        #before submitting the form, while in get method, result is not executed since no post has been done.
        return render_template('register.html', head = 'Registration!', pagetitle = 'Register', user_status = '')



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
            session.permanent = False
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

def rand_id():
    return random.randint(10000000,99999999)

def roomTable(roomID):
    roomdb.createTable(session['username'],roomID)

#page where user chooses to join or create a room.
@app.route('/chatroom', methods = ["GET","POST"])
def chatroomIndex():
    if 'username' in session:
        if request.method == "POST":
            if request.form.get('create'):
                tableId = rand_id()
                roomTable(tableId)
                session['host'] = session['username']
                return redirect(url_for('roomFinal',id=tableId))

            elif request.form.get('join'):
                userEnteredId = request.form['userEnteredId']
                userEnteredHost = request.form['userEnteredHost']
                result = roomdb.connect(session['username'],userEnteredHost,userEnteredId)
                flash (result)
                if result == "Successfully connected to the chatroom!":
                    time.sleep(1)
                    session['host'] = userEnteredHost
                    return redirect(url_for('roomFinal', id = userEnteredId))

                return render_template('chatroom_index.html')
        else:
            return render_template('chatroom_index.html')
    else:
        flash ("Login first to join a chatroom")
        return render_template('home.html')
        
'''
def appendUser(userJoined):
    with open('F:\Vatsal\\text-app\\text-messaging-app\\templates\\roomFinal.html', "r") as html_file:
        soup = Soup(html_file, 'lxml') 
        p_last = soup.find_all("p")[-1]
        if p_last.string == userJoined+' joined the room.':
            p = soup.new_tag('p')
            p.string = userJoined + " joined the room."
            p_last.insert_after(p)
            print(p_last.string, userJoined+' joined the room.')
        
    with open('F:\Vatsal\\text-app\\text-messaging-app\\templates\\roomFinal.html', "w") as f:
        f.write(str(soup.prettify()))'''


@app.route('/room/id=<id>', methods = ["GET","POST"])
def roomFinal(id):
    if 'username' in session:
        #url = request.url
        #id = url[-1:-9:-1][::-1]
        joinedIn = roomdb.joinedUsers(session['host'])
        print(joinedIn)
        #appendUser(session['username'])
        flash (joinedIn)
        return render_template('roomFinal.html',id=id, host = session['host'])
    else:
        return render_template('home.html', info = "Log in first to join a chatroom.")

#get local ip address of the server-host device.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(debug = True, host = ip_address, port = 5000)
