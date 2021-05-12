from flask import Flask, redirect, render_template, request, url_for
import mod_db as mydb

app = Flask(__name__)

def add_data(action,username,password):
    if username != '' and password != '':
        mydb.add(action,username,password)

@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def home():
    return render_template('home.html')


@app.route("/register", methods = ["POST",'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_data('register',username,password)
    return render_template('register.html', head = 'Registration!', pagetitle = 'Register')

@app.route("/login", methods = ["POST",'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_data('login',username,password)
    return render_template('login.html',head = 'Login!', pagetitle = 'Login')

if __name__ == '__main__':
    app.run(debug = True)
