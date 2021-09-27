from flask import Flask, redirect, render_template, request, url_for, session, flash
from bs4 import BeautifulSoup as Soup
import socket
import users_db as userdb
import time, random
import chat_db as roomdb
import numpy as np
import cv2
import subprocess, sys


#pip install pipreqs
#pipreqs . in directory.
def install(path):
    with open(path,'r') as f:
        cont = f.readlines()
        for package in cont:
            print(package[:-2])
            subprocess.check_call([sys.executable, "-m", "pip", "install", package[:-2]])

#install("text-messaging-app-master\\requirements.txt")


host = ''
app = Flask(__name__)
app.secret_key = 'duosandounsaoudasuodousandos'

#reset the roomFinal html final everytime the server is run.

def reset():
    with open ('text-messaging-app-master\\templates\\roomBase.html','r') as f:
        tempCont = f.read()

    with open ('text-messaging-app-master\\templates\\roomFinal.html','w') as f:
        f.write(tempCont)

reset()

class Video():
    count = 0
    users = set()
    def __init__(self, username):
        self.username = username
        Video.users.add(self.username)
        Video.count = len(Video.users)
        
    def showVideo(self):
        self.cap = cv2.VideoCapture(0)

        while True:
            ret, frame = self.cap.read() 
            #cv2.line(image,inital_coord,final_coord,color,thickness)
            img = cv2.line(frame,(0,0),(0,0),(255,0,0),10)
        
            font = cv2.FONT_HERSHEY_SIMPLEX
        
            #cv2.putText(image,text,bottom_left_coord,fontstyle,fontscale,color,thickness,lineType)
            img = cv2.putText(img, 'Press Q to exit', (200,100), font, 1 ,(0,0,0), 4, cv2.LINE_AA)
            img = cv2.putText(img, 'Number of Users: {no}'.format(no = Video.count), (200,50), font, 1 ,(0,0,0), 4, cv2.LINE_AA)
            cv2.imshow('frame', img)
        
            if cv2.waitKey(1) == ord('q'):
                break
            
            
        self.cap.release()
        cv2.destroyAllWindows()


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
                reset()
                return render_template('home.html', info = "User '" + user + "' logged out successfully!")

    elif request.method == 'GET':        
        return render_template('home.html')

#
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

        #empty fields
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

#create a table with a random id, name of table is the hostname.
def roomTable(roomID):
    roomdb.createTable(session['username'],roomID)

#page where user chooses to join or create a room.

@app.route('/joinroom', methods = ['GET', 'POST'])
def joinRoomInput():
    if request.method == "POST":
        userEnteredId = request.form['userEnteredId']
        userEnteredHost = request.form['userEnteredHost']
        result = roomdb.connect(session['username'],userEnteredHost,userEnteredId, host)
        flash (result)
        if result == "Successfully connected to the chatroom!":
            time.sleep(1)
            session['host'] = userEnteredHost
            return redirect(url_for('roomFinal', id = userEnteredId, checkHost = 'host'))
        return render_template('joinRoomInput.html')
    else:
        return render_template('joinRoomInput.html')
    

@app.route('/chatroom', methods = ["GET","POST"])
def chatroomIndex():
    
    #prevent access to chatroom without logging in
    if 'username' in session:
        if request.method == "POST":
            #request.form.get(parameter) for which button clicked
            #parameter is the name of the html element, not its value

            if request.form.get('create'):
                global host
                tableId = rand_id()
                roomTable(tableId)
                #since host created the room
                session['host'] = session['username']
                host = session['host']
                return redirect(url_for('roomFinal',id=tableId, checkHost = 'host'))

            elif request.form.get('join'):
                return redirect(url_for('joinRoomInput'))
                

        else:
            return render_template('chatroom_index.html')

    else:
        flash ("Login first to join a chatroom")
        return render_template('home.html')


def dispMsg(text):
    with open('text-messaging-app-master\\templates\\roomFinal.html', "r") as f:
        soup = Soup(f, 'lxml') 
        #already set a hidden p tag in roomfinal, to use it to add other p tags
        p_last = soup.find_all("p")[-1]
        p = soup.new_tag('p')
        p.string = text
        p_last.insert_after(p)
        

    with open('text-messaging-app-master\\templates\\roomFinal.html', "w") as f:
        f.write(str(soup))

#dont modify this, working on the end button for the chatroom.      
#pip install lxml cuz lxml parser used.  



@app.route('/room/id=<id>', methods = ["GET","POST"])
def roomFinal(id):
    if 'username' in session and 'host' in session:
        joinedIn = roomdb.joinedUsers(session['host'])
        if joinedIn == 'room ended':
            session.pop('username')
            return redirect(url_for('home', info = "Host ended the room."))
        strUsers = ''

        #joinedIn like [(user1,), (user2,),...]
        for joinedUser in joinedIn:
            strUsers += joinedUser[0]+', '

        info = "Current users in the room: " + str(strUsers[:-2])
        showHost = 'Host: ' + str(session['host'])
        showID = 'Room ID: '+str(id)
        flash (info)
        flash(showHost)
        flash (showID)

        if request.form.get('video'):
            curUser = session['username']
            curUser = Video(session['username'])
            curUser.showVideo()
        
        #if enter button pressed (check id of button)
        if request.form.get('enter'):
            msg = request.form['typeMsg']
            if not msg.isspace() and msg != '':
                roomdb.appendMsg(session['username'],msg,session['host'])
                listMsgs = roomdb.get_allMsg(session['host'])
                #reset the roomFinal page, and re-write it with new changes.
                reset()
                #the listMsgs format: [(user1,msg1),(user2,msg2)...]
                
                for content in listMsgs:
                    user = content[0]
                    msg = content[1]
                    combined = user + ': ' + msg
                    dispMsg(combined)
        
        #working on the end button
        elif request.form.get('endButton'):
            reset()
            roomdb.endroom(session['host'])
            session.clear()
            host = ''
            return redirect(url_for('home', info = 'Successfully ended the chatroom!'))
        #if host is on the room page, end button should be visible. not visible for any other user who joins in.
        if session['host'] == session['username']:
            return render_template('roomFinal.html',id=id, host = session['host'], checkHost = 'host')
        else:
            return render_template('roomFinal.html',id=id, host = session['host'], checkHost = 'user')
        #ENDBUTTON WORKING< BUT REMOVE OTHER USERS ALSO.
    else:
        return render_template('home.html', info = "Log in first to join a chatroom.")

#get local ip address of the server-host device.
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(debug = True, host = ip_address)




#REFRESH ONLY DIV, NOT FULL PAGE.