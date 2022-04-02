# text-messaging-app
basic flask thingy
sql connection
login secure
encrypted messaging system


voice recording
files
emoticons


testing from ubuntu
----------------------------
----------------------------
working of the textapp

1) Login:
check what the user inputs as the username and password. the username is stored in the database
along with the password. match the user entered pass and the pass in the db.

2) Register:
check if a username already exists (unique usernames). check if any field is left empty while
registering/logging in. display relevant messages for successful and unsuccessful login/register.

3) Chatroom Index page:
Join or create a chatroom. each chatroom has a unique roomID and a unique host. for joining in, u need to know the host's name and the corresponding roomID to ensure noone randomly slides into a room.

4) Main chatting page:
stored the html of the base of the chatting page in tempRoom.html. everytime the server is hosted, the content of the html file roomFinal.html is replaced with that of the tempRoom.html.
This is because everytime a new message is entered in the chatroom, it gets stored in the database. THe message along with the user who entered that message is pulled from the database and using BeautifulSoup, its added into roomFinal.html. Everytime a new message is entered, the roomFinal.html file is reset to its original form, and the old messages along with the new message is entered as a <p> tag in roomFinal. Its necessary to reset the page everytime cuz otherwise it would cuz it would result in the display of duplicates of the messages. set the page refresh time to anything (set for 5 secs now) so that the changes in the webpage are visible to all the users (or else theyll have to manually refresh the page).

PS: i didnt focus on styling the pages much, thats why its just a bunch of stuff put in the page. but yeah it does work properly nonetheless.
  
----------------------------
----------------------------
  stuff to add/modify
 - 2 diff users can login thru the same device using the same browser (not needed tho, cuz the whole point is to have users chatting from different devices)
 - styling using css, or it can be done later also
 - fixing the refresh feature. for now, the page refreshes every 5 seconds but it should only refresh the div tag which displays the messages.
 - automatically setup the databases and the tables for the user (if the databases and the tables are not yet created for the user)

 NOTE: IF YOU'RE MAKING ANY CHANGE IN ROOMFINAL.HTML, MAKE THE EXACT SAME CHANGE IN ROOMBASE.HTML (EVERY TIME THE SERVER IS RUN, ROOMFINAL GETS RESET TO ROOMBASE.) AND ENSURE THAT WHILE MODIFYING THE FILE, ROOMFINAL HAS THE SAME CONTENT AS ROOMBASE.
  
