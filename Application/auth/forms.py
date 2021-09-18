"""
Login and Registrationn forms
"""
from wtforms import Form, PasswordField, validators, SubmitField, StringField, SelectField


class Registration(Form):
    """ Defines the registration form

    Args:
        Form: Inherits the wtf form libary

    Returns:
        None
    """
    name = StringField("Name:")
    username = StringField("Username:", [validators.DataRequired()])
    phone=StringField("Phone:", [validators.DataRequired()])
    email = StringField('Email Address:', [
                        validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')
    
    submit = SubmitField("Submit")


class Login(Form):
    """ Defines the form used for user login

    Args:
        Form: Inherits the form functions from the wtforms library

    Returns:
        None
    """
    username = StringField("Username:", [validators.DataRequired()])
    password = PasswordField('Your Password', [validators.DataRequired()])
