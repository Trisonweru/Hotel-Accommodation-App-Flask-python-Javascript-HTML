from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators, DecimalField, DateField, TimeField, SubmitField, PasswordField
from datetime import datetime

class Add_Listing(Form):
    name=StringField("Name", [validators.DataRequired()])
    price=StringField("Price",[validators.DataRequired()] )
    discount=IntegerField("Discount", default=0 )
    description=TextAreaField("Description",  [validators.DataRequired()])

    image_1=FileField("Image 1", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png', 'image only please'])])
    image_2=FileField("Image 2", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png', 'image only please'])])
    image_3=FileField("Image 3", validators=[FileRequired(), FileAllowed(['jpg', 'gif', 'jpeg', 'png',  'image only please'])])

class Book(Form):
    days=IntegerField("No of Days", [validators.DataRequired()])
    date_in=DateField('Date in', format='%Y-%m-%d', default=datetime.now())
    time_in=TimeField('Time in', format='%H:%M', default=datetime.now())
    date_out=DateField('Date out', format='%Y-%m-%d', default=datetime.now())
    time_out=TimeField('Time out', format='%H:%M', default=datetime.now())
    submit = SubmitField("Submit")

class AdminUser(Form):
    name=StringField("Name", [validators.DataRequired()])
    username = StringField("Username:", [validators.DataRequired()])
    email = StringField('Email Address:', [
                        validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')
    submit = SubmitField("Submit")

    

