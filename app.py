#Modules
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta

#Config
USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'booking_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'wr%12h.=vxGhf^4qh1KHy?NepeWn+'

#Message Object
class Message(db.Model):
    __tablename__ = 'contact_table'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    message = db.Column(db.String())

#Booking Object
class Booking(db.Model):
    __tablename__ = 'booking_table'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    startTime = db.Column(db.Time())
    endTime = db.Column(db.Time())
    parkSpot = db.Column(db.Integer())
    accountID = db.Column(db.Integer())

    time = str(startTime)[11:]

#Account Object
class Account(db.Model):
    __tablename__ = 'account_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    fullname = db.Column(db.String())
    registration = db.Column(db.String())

#Page Routes
@app.route('/') #Index
def index():
    if not session.get('userId'):
        session['userId'] = 0
    return render_template('index.html', userId=session['userId'])
@app.route('/booking/<error>') #Booking
def booking(error):
    return render_template('booking.html', userId=session['userId'], error=error)
@app.route('/login') #Login
def login():
    return render_template('login.html')
@app.route('/signup') #Signup
def signup():
    return render_template('signup.html')
@app.route('/about') #About
def about():
    return render_template('about.html', userId=session['userId'])
@app.route('/contact/<error>') #Contact
def contact(error):
    return render_template('contact.html', userId=session['userId'], error=error)
@app.route('/tandc') #Terms and Conditions
def tandc():
    return render_template('tandc.html', userId=session['userId'])
@app.route('/thankyou') #Thank You
def thankyou():
    return render_template('thankyou.html')

#Account and Admin Page
@app.route('/account/<error>') #Account
def account(error):
    #User Data
    userAccount = Account.query.filter_by(id=session['userId']).first()
    userName = userAccount.fullname
    userEmail = userAccount.email
    userReg = userAccount.registration
    data = [userName, userEmail, userReg]

    #Booking Data
    bookings = Booking.query.filter_by(accountID=session['userId'])
    futureBookings = bookings.filter(Booking.date >= datetime.today())
    bookingData = [] #Multi-Dimensional Array
    for index in range(len(list(futureBookings))):
        booking = futureBookings[index]
        bookingDataElement = [0, 0, 0, 0, 0, 0]

        bookingDataElement[0] = index + 1               #Booking Index
        bookingDataElement[1] = str(booking.date)       #Booking Date
        bookingDataElement[2] = str(booking.startTime)  #Booking Start Time
        bookingDataElement[3] = str(booking.endTime)    #Booking End Time
        bookingDataElement[4] = booking.parkSpot        #Booking Park Spot
        bookingDataElement[5] = booking.id              #Booking ID

        bookingData.append(bookingDataElement)

    return render_template('account.html', userId=session['userId'], data=data, bookingData=bookingData, error=error)

@app.route('/admin') #Admin
def admin():
    #User Data
    userAccount = Account.query.filter_by(id=session['userId']).first()
    userName = userAccount.fullname
    userEmail = userAccount.email
    userReg = userAccount.registration
    data = [userName, userEmail, userReg]

    #Booking Data
    futureBookings = Booking.query.filter(Booking.date >= datetime.today())
    bookingData = []
    for index in range(len(list(futureBookings))):
        booking = futureBookings[index]
        user = Account.query.filter_by(id=booking.accountID).first()
        bookingDataElement = [0, 0, 0, 0, 0, 0, 0, 0]

        bookingDataElement[0] = user.fullname           #User Name
        bookingDataElement[1] = user.email              #User Email
        bookingDataElement[7] = user.registration       #User Registration
        bookingDataElement[2] = str(booking.date)       #Booking Date
        bookingDataElement[3] = str(booking.startTime)  #Booking Start Time
        bookingDataElement[4] = str(booking.endTime)    #Booking End Time
        bookingDataElement[5] = booking.parkSpot        #Booking Park Spot
        bookingDataElement[6] = booking.id              #Booking ID

        bookingData.append(bookingDataElement)

    #Contact Data
    messages = Message.query.all()
    messageData = []
    for index in range(len(list(messages))):
        message = messages[index]
        messageDataElement = [0, 0, 0, 0]

        messageDataElement[1] = message.fullname    #User Name
        messageDataElement[2] = message.email       #User Email
        messageDataElement[3] = message.message     #Uaer Message
        messageDataElement[0] = message.id          #User ID

        messageData.append(messageDataElement)

    return render_template('admin.html', userId=session['userId'], data=data, bookings=bookingData, messages=messageData)

#Booking Database Connection
@app.route('/submit_booking', methods=['POST']) #Submit Booking
def submit_booking():
    if request.method == 'POST':
        #Form
        date = request.form['date']
        startTime = request.form['time'] + ":00"
        endTime = request.form['endTime'] + ":00"
        parkSpot = int(request.form['parkSpot'])

        #Form Converted to Pyhton DataTypes
        convertedStartTime = datetime.strptime(startTime, "%H:%M:%S")
        convertedDate = datetime.strptime(date, "%Y-%m-%d")
        convertedEndTime = datetime.strptime(endTime, "%H:%M:%S")
        openingTime = datetime.strptime("07:00:00", "%H:%M:%S")
        closingTime =  datetime.strptime("19:00:00", "%H:%M:%S")

        #Errors
        if(parkSpot == 0):                                                          #No Spot Selected
            return redirect('/booking/1')
        if(session['userId'] == 0):                                                 #User Not Logged In
            return redirect('/booking/2')
        if(convertedStartTime < openingTime or convertedStartTime > closingTime):   #Booking Begins Outside Open Hours
            return redirect('/booking/3')
        if(convertedEndTime < openingTime or convertedEndTime > closingTime):       #Booking Ends Outside Open Hours
            return redirect('/booking/4')
        if(convertedEndTime <= convertedStartTime):                                 #Booking Ends before it Begins
            return redirect('/booking/5')
        if(convertedEndTime - convertedStartTime > timedelta(hours=3)):             #Booking longer than 3hrs
            return redirect('/booking/6')
        if(convertedEndTime - convertedStartTime < timedelta(minutes=30)):          #Booking shorter than 30mins
            return redirect('/booking/7')
        if(convertedDate < datetime.now()):                                         #Booking is in past
            if(convertedStartTime <= datetime.now()):
                return redirect('/booking/8')

        #Upload
        newBooking = Booking(date=date, startTime=startTime, endTime=endTime, parkSpot=parkSpot, accountID=session['userId'])
        db.session.add(newBooking)
        db.session.commit()
        return redirect('/') #Thank you page
    return redirect('/booking/0')
@app.route('/deleteBooking/<bookingId>/<destination>') #Delete Booking
def deleteBooking(bookingId, destination):
    booking = Booking.query.filter_by(id=bookingId).first()
    db.session.delete(booking)
    db.session.commit()
    if destination == "1":
        return redirect('/admin')
    return redirect('/account/0')
@app.route('/updateBooking', methods=['POST']) #Update Booking
def updateBooking():
    #Form
    bookingId = request.form['bookingId']
    date = request.form['date']
    startTime = request.form['startTime'] + ":00"
    endTime = request.form['endTime'] + ":00"

    #Check Form Fields Valid
    if not validateDateInput(date) or not validateTimeInput(startTime) or not validateTimeInput(endTime):
        return redirect('/account/1')
    if request.form['spot'] == None or request.form['spot'] == "":
        return redirect('/account/1')

    spot = int(request.form['spot'])

    #Form Converted to Python Datatypes
    convertedStartTime = datetime.strptime(startTime, "%H:%M:%S")
    convertedDate = datetime.strptime(date, "%Y-%m-%d")
    convertedEndTime = datetime.strptime(endTime, "%H:%M:%S")
    openingTime = datetime.strptime("07:00:00", "%H:%M:%S")
    closingTime = datetime.strptime("19:00:00", "%H:%M:%S")

    if (convertedStartTime < openingTime or convertedStartTime > closingTime):  #Booking Begins Outside Open Hours
        return redirect('/account/2')
    if (convertedEndTime < openingTime or convertedEndTime > closingTime):      #Booking Ends Outside Open Hours
        return redirect('/account/3')
    if (convertedEndTime <= convertedStartTime):                                #Booking Ends Before It Begins
        return redirect('/account/4')
    if (convertedEndTime - convertedStartTime > timedelta(hours=3)):            #Booking Is Longer Than 3 Hours
        return redirect('/account/5')
    if (convertedEndTime - convertedStartTime < timedelta(minutes=30)):         #Booking Is Shorter Than 30 Mins
        return redirect('/account/6')
    if (convertedDate < datetime.now()):                                        #Booking Is In The Past
        if (convertedStartTime <= datetime.now()):
            return redirect('/account/7')
    clashedBookings = getClashedBookings(date, convertedStartTime, convertedEndTime)
    if spot in list(clashedBookings):                                           #Parking Spot Clashes with Other Booking
        return redirect('/account/8')

    #Change Booking Data
    booking = Booking.query.filter_by(id=bookingId).first()

    booking.date = date
    booking.startTime = startTime
    booking.endTime = endTime
    booking.parkSpot = spot

    db.session.commit()

    return redirect('/account/0')

#Account Database Connection
@app.route('/submit_signup', methods=['POST']) #Submit Signup
def submit_signup():
    if request.method == 'POST':
        #Form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        registration = request.form['carReg']

        #Errors
        if confirmPassword != password:
            return render_template('signup.html', error=1)      #Passwords are Different
        for account in Account.query.all():
            if account.email == email:
                return render_template('signup.html', error=2)  #Email is Used Already
        if isEmailValid(email) == False:
            return render_template('signup.html', error=3)      #Email is Invalid

        #Password Strength Requirements
        if len(password) < 10:
            return render_template('signup.html', error=4)      #Password Too Short
        passHasUpper = False
        passHasNum = False
        for char in password:
            if char.isupper():
                passHasUpper = True
            if char.isdigit():
                passHasNum = True
        if not passHasUpper:
            return render_template('signup.html', error=5)      #No uppercase letters
        if not passHasNum:
            return render_template('signup.html', error=6)      #No numbers

        #Upload
        newAccount = Account(fullname=name, email=email, password=password, registration=registration)
        db.session.add(newAccount)
        db.session.commit()

        session['userId'] = newAccount.id
        return redirect('/thankyou')
    return render_template('signup.html', error=4)
@app.route('/submit_login', methods=['POST']) #Submit Login
def submit_login():
    if request.method == 'POST':
        #Form
        email = request.form['email']
        password = request.form['password']

        #Errors
        #Is email registered
        validEmail = False
        for account in Account.query.all():
            if account.email == email:
                validEmail = True
        if not validEmail:
            return render_template('login.html', error=1)   #Email Not Registered
        userAccount = Account.query.filter_by(email=email).first()
        #Is password correct
        if userAccount.password != password:
            return render_template('login.html', error=2)   #WrongPassword

        session['userId'] = userAccount.id
        return redirect('/')
    return render_template('login.html', error=3)
@app.route('/deleteAccount') #Delete Account
def deleteAccount():
    user = Account.query.filter_by(id=session['userId']).first()
    db.session.delete(user)
    db.session.commit()
    session['userId'] = 0
    return redirect('/')
@app.route('/logout') #Logout
def logout():
    session['userId'] = 0
    return redirect('/')

#Contact Database Connectivity
@app.route('/submitContact', methods=['POST']) #Submit Message
def submitContact():
    if request.method == 'POST':
        #Form
        name = request.form['name']
        email = request.form['email']
        body = request.form['message']

        #Is email registered
        if isEmailValid(email) == False:
            redirect('contact/1')   #Email Invalid

        #Upload
        newMessage = Message(fullname=name, email=email, message=body)
        db.session.add(newMessage)
        db.session.commit()
        return redirect('/')
    return redirect('contact/0')
@app.route('/deleteMessage/<messageId>') #DeleteMessage
def deleteMessage(messageId):
    message = Message.query.filter_by(id=messageId).first()
    db.session.delete(message)
    db.session.commit()
    return redirect('/admin')

#Other Functions
@app.route('/jsGet', methods=['POST']) #Get Clashed Bookings and Jsonify for Javascript
def jsGet():
    date = request.form['date']
    startTime = datetime.strptime(str(request.form['startTime']) + ":00", "%H:%M:%S")
    endTime = datetime.strptime(str(request.form['endTime']) + ":00", "%H:%M:%S")

    clashedBookings = getClashedBookings(date, startTime, endTime)

    return jsonify(clashedBookings)
def isEmailValid(email: str): #Check For Valid Email
    url = f"https://api.emailvalidation.io/v1/info?email={email}"

    headers = CaseInsensitiveDict()
    headers["apikey"] = "ema_live_P6RRHsE3sEG3UwOfpRChHWtXi940bghNaqJCZhpg"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_resp = response.json()
        format_valid = json_resp["format_valid"]
        mx_found = json_resp["mx_found"]
        smtp_check = json_resp["smtp_check"]
        state = json_resp["state"]

        return format_valid and mx_found and smtp_check and state == "deliverable"

    return False
def validateTimeInput(input): #Check Time Input Is Valid
    try:
        datetime.strptime(input, "%H:%M:%S")
        return True
    except ValueError:
        return False
def validateDateInput(input): #Check Date Input Is Valid
    try:
        datetime.strptime(input, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def getClashedBookings(date, startTime, endTime): #Get Clashed Bookings
    sameDateBookings = Booking.query.filter_by(date=date)
    clashedBookings = []
    for booking in sameDateBookings:

        #Convert Times to Python Datatype
        bookingStartTime = datetime.strptime(str(booking.startTime), "%H:%M:%S")
        bookingEndTime = datetime.strptime(str(booking.endTime), "%H:%M:%S")

        if (bookingStartTime <= endTime) and (bookingEndTime >= endTime):
            clashedBookings.append(booking.parkSpot)
        if (bookingEndTime >= startTime) and (bookingStartTime <= startTime):
            clashedBookings.append(booking.parkSpot)
        if (bookingStartTime <= startTime) and (bookingEndTime >= endTime):
            clashedBookings.append(booking.parkSpot)
        if (bookingStartTime >= startTime) and (bookingEndTime <= endTime):
            clashedBookings.append(booking.parkSpot)

    return clashedBookings