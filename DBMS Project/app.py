from flask import Flask , render_template , request , session , redirect ,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , login_manager , LoginManager
from flask_login import login_required , current_user
from flask_mail import Mail
import json
#we imported flask 


    
#defining local server
local_server = True

app = Flask(__name__)
#here we created object of flask class
app.secret_key='siddhesh'  #optional
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:
# password@localhost/database_table_name'

#this for giving each user its unique access
login_manager=LoginManager(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hospital'
db=SQLAlchemy(app)

#hita testing table cha nav ani class cha nav same pahije nahi tr connect 
#nahi honar , class cha first word capital pahije , nasla capital tari chalel
# class Testing(UserMixin ,db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(50))
#     email=db.Column(db.String(50))

#here we created a route on which
# we will see our website


with open('config.json','r') as c: 
    params=json.load(c)["params"]
    
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT='587',
        MAIL_USER_SSL=True,
        MAIL_USERNAME=params['gmail-user'],
        MAIL_PASSWORD=params['gmail-password']
    )

mail=Mail(app)
    

class User(db.Model , UserMixin):
    user_id=db.Column(db.Integer , primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50) , unique=True)
    password=db.Column(db.String(50))
    
    def get_id(self):
           return (self.user_id)
#here username word given to the function is a variable from signup.html
#in the input tag of username , the data submitted is stored in that 
#name attribute variable and when we use this function request.form.get#
# () it fetches the data and store then in our variables of class

class Patients(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    gender=db.Column(db.String(50))
    slot=db.Column(db.String(50))
    disease=db.Column(db.String(50))
    time=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(50),nullable=False)
    dept=db.Column(db.String(50))
    number=db.Column(db.String(12))
    
    def get_id(self):
           return (self.pid)


class Doctors(db.Model):
    did=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    doctorname=db.Column(db.String(50))
    dept=db.Column(db.String(50))

    
    def get_id(self):
           return (self.pid)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/doctors', methods=['POST','GET'])
@login_required
def doctors():
    if request.method=="POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')
        doctors = Doctors(email=email, doctorname=doctorname, dept=dept)
        db.session.add(doctors)
        db.session.commit()
        flash("Booking Confirmed!!")
    return render_template('doctor.html')

@app.route('/patients' , methods=['POST','GET'])
@login_required
def patients():
    doct=Doctors.query.all()
        
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')
        number=request.form.get('number')
        subject="HOSPITAL MANAGEMENT SYSTEM"
        patients = Patients(email=email, name=name, gender=gender, slot=slot, disease=disease, time=time, date=date, dept=dept, number=number)
        db.session.add(patients)
        db.session.commit()
        
        # mail.send_message(subject, sender=params['gmail_user'],recipients=[email],body=f"Your Booking is CONFIRMED , Thank You")
        flash("Booking Confirmed!!")
        
    return render_template('patient.html',doct=doct)

@app.route('/bookings')
@login_required
def bookings():
    query = Patients.query.filter_by(email=current_user.email).all()
    print(query)
    return render_template('booking.html',query=query)
 

@app.route("/edit/<string:pid>", methods=['POST','GET'])
@login_required
def edit(pid):
    posts = Patients.query.filter_by(pid=pid).first()
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')
        number=request.form.get('number')
        posts.email=email
        posts.name=name
        posts.gender=gender
        posts.slot=slot
        posts.disease=disease
        posts.time=time
        posts.date=date
        posts.dept=dept
        posts.number=number
        db.session.commit()
        Patients.query.all()
        flash("Updated")
        return redirect('/bookings')
    return render_template('edit.html',posts=posts)
    

@app.route("/delete/<string:pid>", methods=['POST','GET'])
@login_required
def delete(pid):
    posts = Patients.query.filter_by(pid=pid).first()
    db.session.delete(posts)
    db.session.commit()
    flash("Deleted")
    return redirect('/bookings')
    

    
@app.route('/signup' , methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username') 
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            print("email already exist's")  
            return render_template('signup.html')
        encpassword=generate_password_hash(password)
        new_user = User(username=username, email=email, password=encpassword)
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')  
    return render_template('signup.html')
         
    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')           #taking email and password from the form variables
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('invalid credentials')
            return render_template('login.html')
        
    return render_template('login.html')

#    print("this is post method")
 #   else :
   #     print("this is get method") 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successfull')
    return redirect(url_for('login'))

# @app.route('/test')
# def test():
#     try:
#         Testing.query.all()
#         return 'Connected'
#     except:
#         return 'not connected'
#     a=Testing.query.all()
#     print(a)


app.run(debug=True)
#we write this command because 
#if we dont write this then we have to write 
#many complicated commands to run this app everytime
