from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.structures import CaseInsensitiveDict

USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'booking_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'pass'

class Booking(db.Model):
    __tablename__ = 'booking_table'
    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime())
    parkLength = db.Column(db.Integer())
    parkSpot = db.Column(db.Integer())
    accountID = db.Column(db.Integer())

class Account(db.Model):
    __tablename__ = 'account_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    fullname = db.Column(db.String())

@app.route('/')
def index():
    return render_template('index.html', userId=session['userId'])

@app.route('/booking')
def booking():
    return render_template('booking.html', userId=session['userId'])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html', userId=session['userId'])

@app.route('/contact')
def contact():
    return render_template('contact.html', userId=session['userId'])

@app.route('/tandc')
def tandc():
    return render_template('tandc.html', userId=session['userId'])

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        #Form
        date = request.form['date']
        time = request.form['time']
        length = request.form['length']
        datetime = date + " " + time + ":00"

        #Upload
        newBooking = Booking(startTime=datetime, parkLength=length, parkSpot=0, accountID=session['userId'])
        db.session.add(newBooking)
        db.session.commit()
        return render_template('index.html') #Thank you page
    return render_template('booking.html')

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
            return render_template('signup.html')
        for account in Account.query.all():
            if account.email == email:
                return render_template('signup.html')
        if isEmailValid(email) == False:
            return render_template('signup.html')

        #Upload
        newAccount = Account(fullname=name, email=email, password=password)
        db.session.add(newAccount)
        db.session.commit()

        session['userId'] = newAccount.id
        return redirect('/thankyou')
    return render_template('signup.html')

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
            return render_template('login.html')
        userAccount = Account.query.filter_by(email=email).first()
        #Is password correct
        if userAccount.password != password:
            return render_template('login.html')

        session['userId'] = userAccount.id
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['userId'] = 0
    return redirect('/')

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
