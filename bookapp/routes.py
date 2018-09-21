from flask import Flask, session, render_template, url_for, flash, redirect, jsonify, request, g, session 
from bookapp import app, Base, engine, dbSession, bcrypt
from bookapp.forms import RegistrationForm, LoginForm
from bookapp.models import User, Review, Book
# 2 - generate database schema
Base.metadata.create_all(engine)

@app.route("/")
@app.route("/home")
def home():
    reg_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('index.html', reg_form=reg_form, login_form=login_form)

@app.route('/register', methods=['post', 'get'])
def register():
    message = None
    reg_form = RegistrationForm()
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('register.html',  reg_form=reg_form, login_form=login_form)

    if request.method == 'POST':
        if reg_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
            dbSession.execute(
                "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                {"username": reg_form.username.data, "email":  reg_form.email.data, "password": hashed_password}
            )
            dbSession.commit()
            return jsonify({'success': 'Registration Successful'})
    return jsonify({'errors': reg_form.errors})

@app.route("/login", methods=['post', 'get'])
def login():
    login_form = LoginForm()
    reg_form = RegistrationForm()
    if request.method == 'GET':
        return render_template('login.html', login_form=login_form,  reg_form=reg_form)

    if request.method == 'POST':
        user = dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": login_form.email.data}
        ).fetchone()

        if login_form.validate_on_submit():
            session.clear()
            session['user_id'] = user['id'] #add user id on session
            return jsonify({'success': 'Login Successful'})
    return jsonify({'errors': login_form.errors})

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = dbSession.execute(
            "SELECT * FROM users WHERE id = :id",
            { "id": user_id }
        ).fetchone()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)