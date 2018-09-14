from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bookapp import dbSession
from bookapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = dbSession.query(User).filter(User.username == username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = dbSession.query(User).filter(User.email == email.data).first()
        if user:
            raise ValidationError('Email already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    login_email = StringField('Email', validators=[DataRequired(), Email()])
    login_password = PasswordField('Password', validators=[DataRequired()])