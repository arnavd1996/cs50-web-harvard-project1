from flask import Flask, session, render_template, url_for, flash, redirect, jsonify, request, g, session 
from bookapp import app, Base, engine, dbSession, bcrypt
from bookapp.forms import RegistrationForm, LoginForm
from bookapp.models import User, Review, Book
# 2 - generate database schema
Base.metadata.create_all(engine)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/register', methods=['post', 'get'])
def register():
    message = None
    reg_form = RegistrationForm()
    if request.method == 'POST':
        if dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": reg_form.email.data}
        ).fetchone() is not None:
            error = 'Email is already registered.'
        elif dbSession.execute(
            "SELECT * FROM users WHERE username = :username",
            {"username": reg_form.username.data}
        ).fetchone() is not None:
            error = 'Username is already registered.'
        elif reg_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
            dbSession.execute(
                "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                {"username": reg_form.username.data, "email":  reg_form.email.data, "password": hashed_password}
            )
            dbSession.commit()
            flash(u'Registration Successful', 'success')
        flash(error, 'danger')
    return render_template('register.html',  reg_form=reg_form)

@app.route("/login", methods=['post', 'get'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        error = None
        user = dbSession.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": login_form.login_email.data}
        ).fetchone()

        if login_form.validate_on_submit():
            if user is None:
                error='Incorrect Username'
            elif not bcrypt.check_password_hash(user.password, login_form.login_password.data):
                error='Incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id'] #add user id on session
            return redirect(url_for('/'))

    return render_template('login.html', error=error)

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
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True)