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

class Item(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

@app.route('/', methods=['GET', 'POST'])
def index():
    items = Item.query.all()
    item_names = []
    for item in items:
        item_names.append(item.name)
    print(item_names)
    return render_template('index.html', items=item_names)

# app = Flask(__name__)
#
# list_of_items = ['moo', 'ma', 'mey']
#
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == "POST":
#         item = request.form['item']
#         list_of_items.append(item)
#     return render_template('index.html', items=list_of_items)

@app.route('/booking')
def booking():
    return render_template('booking.html')