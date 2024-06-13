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
    __tablename__ = 'booking_table'
    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.DateTime)
    parkLength = db.Column(db.Integer)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_id = request.form['item']
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))

    items = Item.query.all()
    return render_template('index.html')