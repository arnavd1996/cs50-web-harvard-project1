from flask import Flask, session, render_template, url_for, flash, redirect, jsonify, request
from bookapp import app, Base, engine, dbSession, bcrypt
from bookapp.forms import RegistrationForm, LoginForm
from bookapp.models import User, Review, Book

# 2 - generate database schema
Base.metadata.create_all(engine)

@app.route("/")
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
        return jsonify({ 'success': 'You have successfully registered' })
    return jsonify({'errors': reg_form.errors})

@app.route("/login", methods=['post'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return jsonify({ 'success': 'no errros!' })
    return jsonify({'errors': login_form.errors})

if __name__ == '__main__':
    app.run(debug=True)