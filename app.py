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
# 4. a Login Page. Done
# 5. a Logout Page. Done
# 6. a Signup page. Done
# 7. a Home Page. Done
# 9. a page to change passwords and user details. 

import math
from flask import Flask, render_template, redirect, url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,current_user,UserMixin,logout_user
from random import randint
from forms import ItemsForm,UserForm,loginForm,Checkout
from werkzeug.security import generate_password_hash,check_password_hash
from flask_bootstrap import Bootstrap4
from datetime import datetime as dt


app = Flask(__name__,
            static_url_path='',
            static_folder='public')

bootstrap = Bootstrap4(app)

#creating the loging manager so it could be used in the login function 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)



db = SQLAlchemy()


app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouserbase.db'

db.init_app(app)

#Creating Tables 
class User(UserMixin,db.Model):
# Main Columns of the table: 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable = False)
    email = db.Column(db.String,unique=True,nullable = False)
    phone = db.Column(db.String(11),unique = True, nullable= False)
    inventory = db.Column(db.String,unique= True, nullable=False)
    address = db.Column(db.String)
    name = db.column(db.String)
    password = db.Column(db.String,nullable= False)
    group = db.Column(db.String)
   # Relationships: 
    items = db.relationship('Items',backref='user',lazy=True)
    order = db.relationship('Orders',backref='user',lazy=True)
    categories = db.relationship('Categories',backref='user',lazy=True)

class Categories(db.Model):
# Main Columns of the table: 
    id = db.Column(db.Integer,primary_key=True)
    category_title = db.Column(db.String)
    shipping_rate_economy = db.Column(db.Float) # The rate giving will be in USD
    shipping_rate_express = db.Column(db.Float)
    # Relationships: 
    items =db.relationship('Items',backref='category_id',lazy=True)
    # Foreign Keys of relationshop
    username =db.Column(db.String, db.ForeignKey(User.id))
    
    
# Creating Items Table. 
class Items(db.Model): 
# Main Columns of the table:
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
    measured_weight = db.Column(db.Float)
    chargeable_weight = db.Column(db.Float)
    item_price = db.Column(db.Float)
    quantity= db.Column(db.Integer,nullable =False)
    scanner = db.Column(db.String)
    # Relationships: 
    order = db.relationship('Orders')
    # Foreign Keys of Relationships: 
    username = db.Column(db.String,db.ForeignKey('user.username'))
    category_title = db.Column(db.String,db.ForeignKey(Categories.id))

# Creating Orders table. 
class Orders(db.Model): 
# Main Columns of the table: 
    id = db.Column(db.Integer,primary_key =True)
    date_created = db.Column(db.Integer,nullable = False)
    first_name = db.Column(db.String,nullable = False)
    last_name =db.Column(db.String,nullable = True)
    phone = db.Column(db.String(11), nullable= False)
    shipping_address = db.Column(db.String)
    order_total = db.Column(db.Float,nullable = False)
    order_weight= db.Column(db.Float,nullable = False)
    inventory = db.Column(db.String)
    payment_method =db.Column(db.String)
    city = db.Column(db.String,nullable=False)
    # Foreign Keys of Relationships: 
    username = db.Column(db.String,db.ForeignKey('user.username'),nullable =False)
    items = db.Column(db.String, db.ForeignKey(Items.id))

with app.app_context():
    db.create_all()


## Home page, 
@app.route('/')
def home(): 
    return render_template('index.html')

## LOGIN / LOGOUT / REGISTER A NEW USER: 
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
            password = generate_password_hash(user_form.password.data,method='pbkdf2',salt_length=18),
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/dashboard')

    return render_template('signup.html',form = user_form)


# Login route
@app.route('/login',methods =['GET','POST'])
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        enterd_password = login_form.password.data
        user = User.query.filter_by(username=login_form.username.data).first()
        if check_password_hash(user.password,enterd_password):
            login_user(user)
            print(f'{user.password}')
            return redirect('/dashboard') # This should be changed to the client dashboard page, not the home page.
        
    return render_template('login.html',form=login_form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


###############################################################################

# This function is suppsed to show the items that are related to the logged in customer only.
@app.route('/dashboard',methods=['Get','Post'])
def client_dashboard():
    items = Items.query.all()
    return render_template('client-dashboard.html',items=items)

from items import *
from cart import *
if __name__ == "__main__": 
    app.run(debug=True)