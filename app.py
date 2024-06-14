from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'booking_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Booking(db.Model):
    __tablename__ = 'booking_table'
    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime())
    parkLength = db.Column(db.Integer())
    parkSpot = db.Column(db.Integer())
    accountID = db.Column(db.Integer())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/tandc')
def tandc():
    return render_template('tandc.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        length = request.form['length']
        datetime = date + " " + time + ":00"
        newBooking = Booking(startTime=datetime, parkLength=length, parkSpot=0, accountID=1)
        db.session.add(newBooking)
        db.session.commit()
        return render_template('index.html') #Thank you page
    return render_template('booking.html')