from flask import Flask , render_template , request , session , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , login_manager
#we imported flask 

#defining local server
local_server = True

app = Flask(__name__)
#here we created object of flask class
app.secret_key='siddhesh'  #optional
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:
# password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hospital'
db=SQLAlchemy(app)

#hita testing table cha nav ani class cha nav same pahije nahi tr connect 
#nahi honar , class cha first word capital pahije , nasla capital tari chalel
class Testing(UserMixin ,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))

#here we created a route on which
# we will see our website

@app.route('/')
def hello():
    return render_template('index.html')
    
@app.route('/doctor')
def doctors():
    return render_template('doctor.html')

@app.route('/patient')
def patients():
    return render_template('patient.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

class User(db.Model):
    user_id=db.Column(db.Integer , primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50) , unique=True)
    password=db.Column(db.String(50))
#here username word given to the function is a variable from signup.html
#in the input tag of username , the data submitted is stored in that 
#name attribute variable and when we use this function request.form.get#
# () is fetches the data and store then in our variables of class
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
         
    

@app.route('/login')
def login():
    return render_template('login.html')

#    print("this is post method")
 #   else :
   #     print("this is get method") 

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/test')
def test():
    try:
        Testing.query.all()
        return 'Connected'
    except:
        return 'not connected'
    a=Testing.query.all()
    print(a)


app.run(debug=True)
#we write this command because 
#if we dont write this then we have to write 
#many complicated commands to run this app everytime
