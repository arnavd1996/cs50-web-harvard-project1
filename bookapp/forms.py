from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bookapp import dbSession, bcrypt
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": email.data}
        ).fetchone()
        if user is None:
            raise ValidationError('Incorrect Email.')
    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        user = dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": self.email.data}
        ).fetchone()
        if not bcrypt.check_password_hash(user.password, self.password.data):
            self.password.errors.append('Incorrect Password.')
            return False
        return True

class SearchForm(FlaskForm):
    searchText = StringField('Search Books', validators=[DataRequired()])
