from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuration for bcrypt
app.config['SECRET_KEY'] = '/!@#$%^&*()gpb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pnrvnavoxvnlgw:4e404dad909373387cd7b0a473b85dce9f66dd1c344e7166f453efab0197c1c5@ec2-50-16-196-138.compute-1.amazonaws.com:5432/dc30a3q121n058'
bcrypt = Bcrypt(app)

# login_manager
login_manager = LoginManager(app)

engine = create_engine('postgres://pnrvnavoxvnlgw:4e404dad909373387cd7b0a473b85dce9f66dd1c344e7166f453efab0197c1c5@ec2-50-16-196-138.compute-1.amazonaws.com:5432/dc30a3q121n058')
# db = scoped_session(sessionmaker(bind=engine))
DbSession = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

# create a Session
dbSession = DbSession()

from bookapp import routes