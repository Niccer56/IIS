from dpmb import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # TODO encryption
    type = db.Column(db.String(20), nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    linkid = db.Column(db.Integer, db.ForeignKey("link.id"), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #maybe pickletype for start and finish instead of FKs?
    start = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    end = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkid = db.Column(db.Integer, db.ForeignKey("link.id"), nullable=False)
    current_station = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
