from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,FloatField,SubmitField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired

egypt_governorates = [
    'Alexandria', 
    'Aswan', 
    'Asyut', 
    'Beheira', 
    'Beni Suef', 
    'Cairo', 
    'Dakahlia', 
    'Damietta', 
    'Faiyum', 
    'Gharbia', 
    'Giza', 
    'Ismailia', 
    'Kafr El Sheikh', 
    'Luxor', 
    'Matrouh', 
    'Minya', 
    'Monufia', 
    'New Valley', 
    'North Sinai', 
    'Port Said', 
    'Qalyubia', 
    'Qena', 
    'Red Sea', 
    'Sharqia', 
    'Sohag', 
    'South Sinai', 
    'Suez'
]

class UserForm(FlaskForm): 
    username = StringField('username',validators=[DataRequired()])
    email = EmailField('email',validators=[DataRequired()])
    phone = StringField('Phone',validators = [DataRequired()])
    address = StringField('address',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Singup')

class ItemsForm(FlaskForm): 
    tracking_number = StringField('Tracking #',validators=[DataRequired()])
    username = StringField('Inventory Username')
    item_weight = FloatField('Item Weight',validators=[DataRequired()])
    scanning_country= StringField('Country',validators=[DataRequired()])
    item_category = StringField('Item Category')

    submit =SubmitField('Add Item')


class loginForm(FlaskForm): 
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    login = SubmitField('Login')

class Checkout(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    phone = IntegerField('Phone Number',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    payment_method = StringField('Payment Method',validators=[DataRequired()])
    city = SelectField('City',choices=egypt_governorates)
    username = StringField('Username',validators=[DataRequired()])
