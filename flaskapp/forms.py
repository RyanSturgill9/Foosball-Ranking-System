from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length

class Register(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25),])
    email = EmailField('Email', validators=[
        DataRequired(),
        Length(min=6, max=35),])
    display_name = StringField('Display name', validators=[
        DataRequired(),
        Length(min=4, max=25)])
    firstname = StringField('First name', validators=[
        DataRequired(),
        Length(max=15),])
    lastname = StringField('Last name', validators=[
        DataRequired(),
        Length(max=30),])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords do not match'),
        Length(min=20, max=100, message='Password must be between 20 and 100 characters'),])
    confirm_password = PasswordField('Repeat Password')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class Game(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
