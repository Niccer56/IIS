from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_authorize import Authorize
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__, instance_relative_config=True)

#https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls - for setup of own db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://michal:whiskeyindianovember@winess.irineva.nyara.network:3360/IIS'
app.config['SECRET_KEY'] = os.urandom(32) #enable to work with forms

login_manager = LoginManager(app)
db = SQLAlchemy(app)
authorize = Authorize(app)
bcrypt = Bcrypt(app)

from dpmb import models
