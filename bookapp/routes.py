from flask import Flask, session, render_template, url_for, flash, redirect, jsonify, request, g, session 
from bookapp import app, Base, engine, dbSession, bcrypt
from bookapp.forms import RegistrationForm, LoginForm
from bookapp.models import User, Review, Book
import requests
import datetime

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

@app.route("/search", methods=['get', 'post'])
def search():
    if request.method == 'POST':
        text = request.form.get("searchText")
        print(text)
        result = dbSession.execute(
            "SELECT * FROM books WHERE (LOWER(isbn) LIKE LOWER(:text)) OR (LOWER(title) LIKE LOWER(:text)) OR (author LIKE LOWER(:text)) LIMIT 10",
            { "text": '%' + text + '%'} 
        ).fetchall()
        print(result)
        data = []
        for row in result:
            data.append(dict(row))
        return jsonify({ 'data': data })

@app.route("/book/<isbn>", methods=['get', 'post'])
def book(isbn):
    login_form = LoginForm()
    reg_form = RegistrationForm()
    if request.method == 'GET':
        voted = None
        userId = session.get('user_id')
        book = dbSession.execute(
            "SELECT * FROM books WHERE isbn = :isbn",
            { "isbn": isbn }
        ).fetchone()
        if book is not None:
            user = dbSession.execute(
                "SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id",
                { "book_id": book['id'], "user_id": userId }
            ).fetchone()
            print(user)
            voted=bool(user)
            print(voted)
        return render_template("book.html", book=book, voted=voted, login_form=login_form,  reg_form=reg_form)
    # if request.method == 'POST':
    #     rating = request.form.get("rating")
    #     content = request.form.get("content")
    #     book_id = request.form.get("book-id")
    #     user_id = session.get('user_id')
    #     date_posted = datetime.datetime.now()
    #     dbSession.execute(
    #         "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
    #         {"username": reg_form.username.data, "email":  reg_form.email.data, "password": hashed_password}
    #     )
    #     dbSession.commit()
    #     return jsonify({ 'data': 'a'})

@app.route("/addreview", methods=['get', 'post'])
def addreview():
    if request.method == 'POST':
        req_data = request.get_json()
        rate = req_data['rate']
        text = req_data['text']
        userId = req_data['userId']
        bookId = req_data['bookId']
        dt = datetime.datetime.now()
        dbSession.execute(
            "INSERT INTO reviews (content, date_posted, user_id, book_id, rating) VALUES (:content, :date_posted, :user_id, :book_id, :rating)",
            {"content": text, "date_posted":  dt, "user_id": userId, "book_id": bookId, "rating": rate }
        )
        dbSession.commit()
        return jsonify({'OK': 'SUCCESS'})

# @app.route("/api/<int:isbn>")
# def flight(isbn):
#     # Make sure flight exists.
#     res = requests.get(
#         "https://www.goodreads.com/book/review_counts.json",
#         params={ "key": "KEY", "isbns": isbn }
#     )
#     book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
#     if book is None:
#         return render_template("book.html", message="No such flight.")

#     # Get all passengers.
#     passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
#                             {"flight_id": flight_id}).fetchall()
#     return render_template("flight.html", flight=flight, passengers=passengers)


if __name__ == '__main__':
    app.run(debug=True)