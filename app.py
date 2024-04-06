# This is a warhousing and fulfillment application. 
# The app is supposed to organize the Sending and Receiving process of the packages in the warehouse. 
# The features of this app should be as follows: 
## the The received items should be logged in the system, each in it's own inventory. 
## The client should be able to see his items and the tracking process of it. 
## The client should be able to order a shipping label once the itmes is delivered to the final address, and make a payment. 
## each inventory should have a random number generated, to be added as an address line. 


# To do this is should contanint the following: 
# 1. a Dashboard for the client. 
# 2. a Dashboard for the employee. 
# 3. a Checkout Page. 
# 4. a Login Page. 
# 5. a Logout Page. 
# 6. a Signup page. 
# 7. a Home Page. 
# 9. a page to change passwords and user details. 

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from random import randint
from forms import ItemsForm,UserForm
from flask_migrate import Migrate
app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate(app,db)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouserbasa.db'

db.init_app(app)

#Creating Tables 
class User(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable = False)
    email = db.Column(db.String,unique=True,nullable = False)
    phone = db.Column(db.String(11),unique = True, nullable= False)
    inventory = db.Column(db.String,unique= True, nullable=False)
    address = db.Column(db.String)
    name = db.column(db.String)
    items = db.relationship('Items',backref='user',lazy=True)
    order = db.relationship('Orders',backref='user',lazy=True)
    password = db.Column(db.String,nullable= False)

class Items(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    tracking_number = db.Column(db.String, nullable =False)
    source_country = db.Column(db.String, nullable = False)
    receiving_date = db.Column(db.String, nullable =False)
    shipping_date = db.Column(db.String)
    transit_date = db.Column(db.String)
    to_destination_date = db.Column(db.String)
    local_warehouse_date = db.Column(db.String)
    ofd_date = db.Column(db.String)
    delivered_date = db.Column(db.String)
    weight = db.Column(db.Float)
    scanner = db.Column(db.String)
    username = db.Column(db.String,db.ForeignKey('user.username'),nullable=False)

class Orders(db.Model): 
    
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String,db.ForeignKey('user.username'),nullable =False)

with app.app_context():
    db.create_all()


## Home page, 
@app.route('/')
def home(): 
    return render_template('index.html')

#Sign up page. 
@app.route('/signup',methods=['GET','POST'])
def signup(): 
    user_form = UserForm()
    if user_form.validate_on_submit(): 

        print(user_form.name.data)
        user =    User(
            username = user_form.username.data,
            name = user_form.name.data,
            email = user_form.email.data,
            address = user_form.address.data,
            phone = user_form.phone.data,
            inventory = str(f'SHP-{randint(1000,9999)}'),
            password = user_form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('signup.html',form = user_form)









if __name__ == "__main__": 
    app.run(debug=True)