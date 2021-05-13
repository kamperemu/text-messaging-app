from flask import Flask, redirect, render_template, request, url_for
import mod_db as mydb
import socket

app = Flask(__name__)


def add_data(action,username,password):
    if username != '' and password != '':
        return(mydb.add(action,username,password))


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
    return render_template('home.html')


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
        return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = result)
    else:
        return render_template('login.html',head = 'Login!', pagetitle = 'Login', user_status = '')


#get local ip address of the server-host device.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(debug = True, host = ip_address, port = 5000)

#MY IP ADDRESS: 192.168.100.3