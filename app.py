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
isInterviewsPressed = True

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

@app.route("/submitSt", methods=['POST', 'GET'])
def submitSt():
    if request.method=='POST':
        sender_email="yfeg2024@hotmail.com"

        subject = "ავთენტიფიკაცია"
        body='გამარჯობა, \n გიგზავნით ავთენტიფიკაციისთვის საჭირო კითხვარს. კითხვარის შევსების შემდგომ ჩვენი გუნდი გადაამოწმებს პასუხებს და დაგიკავშირდებათ შესაძლო მასპინძლის გამოჩენისას. \n https://forms.gle/ysdv1W4b4mR3cZ5L7 \n პატივისცემით „ახალგაზრდები ევროპისთვის“'

        name=request.form.get('name')
        surname=request.form.get('surname')
        city=request.form.get('city')
        email=request.form.get('email')
        receiver_email=email


        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        

        # SMTP server configuration
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587  # For TLS
        smtp_username = "yfeg2024@hotmail.com"
        smtp_password = "Dacva100"
        msg.attach(MIMEText(body, 'plain'))


         #Sending the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully სტუმ!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()



        if any(field == '' for field in [name, email, city, surname] ) or ("@" not in email) or (db.session.query(stumari).filter_by(email=email).first() is not None):
            return '''
            <h1>არასწორადაა შევსებული.</h1>
            <form action="/" method="get">
                <button type="submit">დაბრუნდი</button>
            </form>
            ''' 
        else:
            import random
            global idx
            idx = random.randint(100000, 999999)
            new_stumari = stumari(name=name, surname=surname, email=email, city=city,  idx=idx)
            try:
                db.session.add(new_stumari)
                db.session.commit()
            except Exception as e:
                return 'There was an issue with the database: {}'.format(str(e))
            return redirect("/inter")
    

@app.route("/submitMs", methods=['POST', 'GET'])
def submitMs():
    if request.method=='POST':
        sender_email="yfeg2024@hotmail.com"
        subject = "ავთენტიფიკაცია"
        body='გამარჯობა, \n გიგზავნით ავთენტიფიკაციისთვის საჭირო კითხვარს. კითხვარის შევსების შემდგომ ჩვენი გუნდი გადაამოწმებს პასუხებს და დაგიკავშირდებათ შესაძლო სტუმრის გამოჩენისას. \n https://forms.gle/299VvqPECVsehcjt9 \n პატივისცემით „ახალგაზრდები ევროპისთვის“'

        name=request.form.get('name')
        surname=request.form.get('surname')
        city=request.form.get('city')
        email=request.form.get('email')
        receiver_email=email

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # SMTP server configuration
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587  # For TLS
        smtp_username = "yfeg2024@hotmail.com"
        smtp_password = "Dacva100"
        msg.attach(MIMEText(body, 'plain'))

        # Sending the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()




        if any(field == '' for field in [name, email, city, surname] ) or ("@" not in email) or (db.session.query(maspinzeli).filter_by(email=email).first() is not None):
            return '''
            <h1>არასწორადაა შევსებული.</h1>
            <form action="/" method="get">
                <button type="submit">დაბრუნდი</button>
            </form>
            '''
        else:
            import random
            global idx
            idx = random.randint(100000, 999999)
            new_maspinzeli = maspinzeli(name=name, surname=surname, email=email, city=city,  idx=idx)
            try:
                db.session.add(new_maspinzeli)
                db.session.commit()
            except Exception as e:
                return 'There was an issue with the database: {}'.format(str(e))
            return redirect("/inter")

@app.route("/archevnebi")
def masp():
    return render_template('arch.html.j2')
    
@app.route("/admin", methods=['POST', 'GET'])
def admin():
    if request.method=='POST':
        checkbox = request.form.get('checkbox')
        is_yt2 = bool(checkbox == 'on')
        password = request.form.get('password')
        filename = request.form.get('filename')
        title = request.form.get('title')
        body = request.form.get('body-text')

        if password is None or password != "n378asD":
            return "<a href='/admin'>Incorrect password</a>"
        
        if any(field is None for field in [filename, title, body]):
            return 'Missing required fields'

        new_stat = stat(is_yt=is_yt2, filename=filename, title=title, content=body)
        try:
            db.session.add(new_stat)
            db.session.commit()
        except Exception as e:
            return 'There was an issue with the database: {}'.format(str(e))
        return redirect("/")

    else:
        return render_template('admin.html.j2')

@app.route("/statia/<id>")
def statia(id):
    entry = stat.query.get(id)
    return render_template('stat.html.j2', entry=entry)

@app.route("/inter")
def inter():
    return render_template('inter.html.j2', idx=idx)

@app.route("/about")
def about():
    return render_template('about.html.j2')

if __name__ == "__main__":
    app.run(debug=True)

