from flask import Flask, session, render_template, url_for, flash, redirect, jsonify, request
from bookapp import app, Base, engine, dbSession, bcrypt
from bookapp.forms import RegistrationForm, LoginForm
from bookapp.models import User, Review, Book
from flask_login import login_user, current_user, logout_user
# 2 - generate database schema
Base.metadata.create_all(engine)

@app.route("/", endpoint='/')
def index():
    reg_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index.html', reg_form=reg_form, login_form=login_form)

@app.route('/register/', methods=['post'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        dbSession.add(User(reg_form.username.data, reg_form.email.data, hashed_password))
        dbSession.commit()
        dbSession.close()
        return jsonify({'errors': None })
    return jsonify({'errors': reg_form.errors})

@app.route("/login", methods=['post'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = dbSession.query(User).filter(User.email == login_form.login_email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.login_password.data):
            login_user(user)
            return redirect(url_for('/'))
        else:
            return jsonify({'error': 'Login Failed'})

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('/'))

if __name__ == '__main__':
    app.run(debug=True)