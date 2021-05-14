from flask import Flask, redirect, render_template, request, url_for, session
import mod_db as mydb
import socket

app = Flask(__name__)
app.secret_key = 'duosandounsaoudasuodousandos'

def add_data(action,username,password):
    if username != '' and password != '':
        return(mydb.add(action,username,password,session))


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

@app.route("/login", methods = ["POST",'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = add_data('login',username,password)
        if result == "Login successful!" and session.get('username') is None:
            session['username'] = username
            session['password'] = password
        print(username,password,session)
        return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = result)
           
    else:
        return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = '')


#get local ip address of the server-host device.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(debug = True, host = ip_address, port = 5000)

#MY IP ADDRESS: 192.168.100.3