from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests, json
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta

USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'booking_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'wr%12h.=vxGhf^4qh1KHy?NepeWn+'

class Message(db.Model):
    __tablename__ = 'contact_table'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    message = db.Column(db.String())

class Booking(db.Model):
    __tablename__ = 'booking_table'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    startTime = db.Column(db.Time())
    endTime = db.Column(db.Time())
    parkSpot = db.Column(db.Integer())
    accountID = db.Column(db.Integer())

    time = str(startTime)[11:]

class Account(db.Model):
    __tablename__ = 'account_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    fullname = db.Column(db.String())

@app.route('/')
def index():
    if not session.get('userId'):
        session['userId'] = 0
    print(session['userId'])
    return render_template('index.html', userId=session['userId'])

@app.route('/booking/<error>')
def booking(error):
    return render_template('booking.html', userId=session['userId'], error=error)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html', userId=session['userId'])

@app.route('/contact/<error>')
def contact(error):
    return render_template('contact.html', userId=session['userId'], error=error)

@app.route('/tandc')
def tandc():
    return render_template('tandc.html', userId=session['userId'])

@app.route('/account/<error>')
def account(error):
    userAccount = Account.query.filter_by(id=session['userId']).first()
    userName = userAccount.fullname
    userEmail = userAccount.email
    data = [userName, userEmail]
    
    bookings = Booking.query.filter_by(accountID=session['userId'])
    futureBookings = bookings.filter(Booking.date >= datetime.today())
    bookingData = []
    for index in range(len(list(futureBookings))):
        booking = futureBookings[index]
        bookingDataElement = [0, 0, 0, 0, 0, 0]

        bookingDataElement[0] = index + 1
        bookingDataElement[1] = str(booking.date)
        bookingDataElement[2] = str(booking.startTime)
        bookingDataElement[3] = str(booking.endTime)
        bookingDataElement[4] = booking.parkSpot
        bookingDataElement[5] = booking.id

        bookingData.append(bookingDataElement)

    return render_template('account.html', userId=session['userId'], data=data, bookingData=bookingData, error=error)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        #Form
        date = request.form['date']
        startTime = request.form['time'] + ":00"
        endTime = request.form['endTime'] + ":00"
        parkSpot = int(request.form['parkSpot'])

        convertedStartTime = datetime.strptime(startTime, "%H:%M:%S")
        convertedDate = datetime.strptime(date, "%Y-%m-%d")
        convertedEndTime = datetime.strptime(endTime, "%H:%M:%S")
        openingTime = datetime.strptime("07:00:00", "%H:%M:%S")
        closingTime =  datetime.strptime("19:00:00", "%H:%M:%S")

        #Errors
        if(parkSpot == 0):
            return redirect('/booking/1')
        if(session['userId'] == 0):
            return redirect('/booking/2')
        if(convertedStartTime < openingTime or convertedStartTime > closingTime):
            return redirect('/booking/3')
        if(convertedEndTime < openingTime or convertedEndTime > closingTime):
            return redirect('/booking/4')
        if(convertedEndTime <= convertedStartTime):
            return redirect('/booking/5')
        if(convertedEndTime - convertedStartTime > timedelta(hours=3)):
            return redirect('/booking/6')
        if(convertedEndTime - convertedStartTime < timedelta(minutes=30)):
            return redirect('/booking/7')
        if(convertedDate < datetime.now()):
            if(convertedStartTime <= datetime.now()):
                return redirect('/booking/8')

        #Upload
        newBooking = Booking(date=date, startTime=startTime, endTime=endTime, parkSpot=parkSpot, accountID=session['userId'])
        db.session.add(newBooking)
        db.session.commit()
        return redirect('/') #Thank you page
    return redirect('/booking/0')

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    if request.method == 'POST':
        #Form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        #Errors
        if confirmPassword != password:
            return render_template('signup.html', error=1)
        for account in Account.query.all():
            if account.email == email:
                return render_template('signup.html', error=2)
        if isEmailValid(email) == False:
            return render_template('signup.html', error=3)
        if len(password) < 10:
            return render_template('signup.html', error=4)
        passHasUpper = False
        passHasNum = False
        for char in password:
            if char.isupper():
                passHasUpper = True
            if char.isdigit():
                passHasNum = True
        if not passHasUpper:
            return render_template('signup.html', error=5)
        if not passHasNum:
            return render_template('signup.html', error=6)

        #Upload
        newAccount = Account(fullname=name, email=email, password=password)
        db.session.add(newAccount)
        db.session.commit()

        session['userId'] = newAccount.id
        return redirect('/thankyou')
    return render_template('signup.html', error=4)

@app.route('/submit_login', methods=['POST'])
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
            return render_template('login.html', error=1)
        userAccount = Account.query.filter_by(email=email).first()
        #Is password correct
        if userAccount.password != password:
            return render_template('login.html', error=2)

        session['userId'] = userAccount.id
        return redirect('/')
    return render_template('login.html', error=3)

@app.route('/logout')
def logout():
    session['userId'] = 0
    return redirect('/')

@app.route('/deleteBooking/<bookingId>')
def deleteBooking(bookingId):
    booking = Booking.query.filter_by(id=bookingId).first()
    db.session.delete(booking)
    db.session.commit()
    return redirect('/account/0')

@app.route('/deleteAccount')
def deleteAccount():
    user = Account.query.filter_by(id=session['userId']).first()
    db.session.delete(user)
    db.session.commit()
    session['userId'] = 0
    return redirect('/')

@app.route('/updateBooking', methods=['POST'])
def updateBooking():
    bookingId = request.form['bookingId']
    date = request.form['date']
    startTime = request.form['startTime'] + ":00"
    endTime = request.form['endTime'] + ":00"

    if not validateDateInput(date) or not validateTimeInput(startTime) or not validateTimeInput(endTime):
        return redirect('/account/1')
    if request.form['spot'] == None or request.form['spot'] == "":
        return redirect('/account/1')

    spot = int(request.form['spot'])

    convertedStartTime = datetime.strptime(startTime, "%H:%M:%S")
    convertedDate = datetime.strptime(date, "%Y-%m-%d")
    convertedEndTime = datetime.strptime(endTime, "%H:%M:%S")
    openingTime = datetime.strptime("07:00:00", "%H:%M:%S")
    closingTime = datetime.strptime("19:00:00", "%H:%M:%S")

    if (convertedStartTime < openingTime or convertedStartTime > closingTime):
        return redirect('/account/2')
    if (convertedEndTime < openingTime or convertedEndTime > closingTime):
        return redirect('/account/3')
    if (convertedEndTime <= convertedStartTime):
        return redirect('/account/4')
    if (convertedEndTime - convertedStartTime > timedelta(hours=3)):
        return redirect('/account/5')
    if (convertedEndTime - convertedStartTime < timedelta(minutes=30)):
        return redirect('/account/6')
    if (convertedDate < datetime.now()):
        if (convertedStartTime <= datetime.now()):
            return redirect('/account/7')
    clashedBookings = getClashedBookings(date, convertedStartTime, convertedEndTime)
    if spot in list(clashedBookings):
        return redirect('/account/8')

    booking = Booking.query.filter_by(id=bookingId).first()

    booking.date = date
    booking.startTime = startTime
    booking.endTime = endTime
    booking.parkSpot = spot

    db.session.commit()

    return redirect('/account/0')

@app.route('/submitContact', methods=['POST'])
def submitContact():
    if request.method == 'POST':
        #Form
        name = request.form['name']
        email = request.form['email']
        body = request.form['message']

        #Is email registered
        validEmail = False
        for account in Account.query.all():
            if account.email == email:
                validEmail = True
        if not validEmail:
            redirect('contact/1')

        newMessage = Message(fullname=name, email=email, message=body)
        db.session.add(newMessage)
        db.session.commit()
        return redirect('/')
    return redirect('contact/0')

@app.route('/jsGet', methods=['POST'])
def jsGet():
    date = request.form['date']
    startTime = datetime.strptime(str(request.form['startTime']) + ":00", "%H:%M:%S")
    endTime = datetime.strptime(str(request.form['endTime']) + ":00", "%H:%M:%S")

    clashedBookings = getClashedBookings(date, startTime, endTime)

    return jsonify(clashedBookings)


def isEmailValid(email: str):
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

def validateTimeInput(input):
    try:
        datetime.strptime(input, "%H:%M:%S")
        return True
    except ValueError:
        return False

def validateDateInput(input):
    try:
        datetime.strptime(input, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def getClashedBookings(date, startTime, endTime):
    sameDateBookings = Booking.query.filter_by(date=date)
    clashedBookings = []
    for booking in sameDateBookings:

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