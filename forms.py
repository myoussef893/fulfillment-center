from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,FloatField,SubmitField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired
source_countries = ['','US','UK','UAE','CN']
status = ['Received in origin warehouse','Ready for International Shipping','Shipped Internationlly','In Transit','In Customs',"Received at Destination Country's warehouse",'Out for delivery','Deliverd']
egypt_governorates = ['',
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

payment_method = ['','Cash On Delivery','Bank Deposit',"Credit Card"]



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
    username = StringField('Username',validators=[DataRequired()])
    item_weight = FloatField('Item Weight',validators=[DataRequired()])
    scanning_country= SelectField('Country',validators=[DataRequired()],choices=source_countries)
    item_category = StringField('Item Category')
    status = SelectField('Status',choices=status,validators=[DataRequired()])
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
    city = SelectField('City',choices=egypt_governorates)
    payment_method = SelectField('Payment Method',choices=payment_method)
    
    submit = SubmitField('Compelete Order')