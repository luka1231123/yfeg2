from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
db=SQLAlchemy(app)

idx=0
isInterviewsPressed = False

class stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(100000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    is_yt = db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return '<Content %r>' % self.id
    
class maspinzeli(db.Model):


    name = db.Column(db.String(500), nullable=False)
    surname = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    idx = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return '<Content %r>' % self.id
    
class stumari(db.Model):


    name = db.Column(db.String(500), nullable=False)
    surname = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    idx = db.Column(db.Integer, primary_key=True)



    def __repr__(self):
        return '<Content %r>' % self.id
    
@app.route("/")
def index():
    if(isInterviewsPressed):
        stats = stat.query.order_by(stat.date_created).filter_by(is_yt=True).all()
    else:
        stats = stat.query.order_by(stat.date_created).filter_by(is_yt=False).all()
    entries_length = len(stats)
    return render_template('index.html.j2', stats=stats, entries_length=entries_length, isInterviewsPressed=isInterviewsPressed)

@app.route("/1")
def index1():
    global isInterviewsPressed
    isInterviewsPressed = True
    return redirect("/")
@app.route("/2")
def index2():
    global isInterviewsPressed
    isInterviewsPressed = False
    return redirect("/")

@app.route("/statia/<id>")
def statia(id):
    entry = stat.query.get(id)
    return render_template('stat.html.j2', entry=entry)


@app.route("/about")
def about():
    return render_template('about.html.j2')

if __name__ == "__main__":
    app.run(debug=True)

