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
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = dbSession.execute(
            "SELECT * FROM users WHERE username = :username",
            {"username": username.data}
        ).fetchone()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": email.data}
        ).fetchone()
        if user:
            raise ValidationError('Email already taken.')

class LoginForm(FlaskForm):
    login_email = StringField('Email', validators=[DataRequired(), Email()])
    login_password = PasswordField('Password', validators=[DataRequired()])
    login_submit = SubmitField('Login')