from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://michal:whiskeyindianovember@winess.irineva.nyara.network:3360/IIS'
app.config['SECRET_KEY'] = os.urandom(32) #enable to work with forms

db = SQLAlchemy(app)

from dpmb import models