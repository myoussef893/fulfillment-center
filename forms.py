from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,FloatField,SubmitField,PasswordField
from wtforms.validators import DataRequired

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
    inventory = StringField('Inventory ID')
    item_weight = FloatField('Item Weight',validators=[DataRequired()])