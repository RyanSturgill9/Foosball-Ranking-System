from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class GameForm(FlaskForm):
    player1_id = IntegerField('Player 1 ID', validators=[DataRequired()])
    player1_score = IntegerField('Player 1 score', validators=[DataRequired()])
    player2_id = IntegerField('Player 2 ID', validators=[DataRequired()])
    player2_score = IntegerField('Player 2 score', validators=[DataRequired()])
    referee_id = IntegerField('Referee ID', validators=[DataRequired()])