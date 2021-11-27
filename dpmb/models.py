from dpmb import db, bcrypt
from flask_login import UserMixin
from flask_authorize import AllowancesMixin


UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    def getAllRoles():
        query = Role.query.all()
        names = []
        for role in query:
            names.append(role.name)
        return names
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    roles = db.relationship('Role', secondary=UserRole)

    def password_check(self, unhashed_pwd):
        return bcrypt.check_password_hash(self.password, unhashed_pwd)

    def getAllCarriersName():
        carriers = User.query.join(User.roles).filter_by(name="carrier").all()
        names = []
        for carrier in carriers:
            names.append(f"{carrier.email}")
        return names

    def getAllEmails():
        query = User.query.all()
        names = []
        for user in query:
            names.append(user.email)
        return names

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    linkid = db.Column(db.Integer, db.ForeignKey("link.id"), nullable=False)
    expiration = db.Column(db.DateTime)

class StationLink(db.Model):
    __tablename__ = 'station_link'
    station_id = db.Column(db.ForeignKey('station.id'), primary_key=True)
    link_id = db.Column(db.ForeignKey('link.id'), primary_key=True)
    time = db.Column(db.DateTime)
    station = db.relationship("Station", back_populates="links")
    link = db.relationship("Link", back_populates="stations")
    def getAllStations():
        query = StationLink.query.all()
        names = []
        for station in query:

            names.append((station.station.name + " " + station.time.strftime("%m/%d/%Y %H:%M")))
        return names
class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    links = db.relationship("StationLink", back_populates="station")

    

    def getAllStationNames():
        query = Station.query.all()
        names = []
        for station in query:
            names.append(station.name)
        return names

class Link(db.Model):
    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True)
    #maybe pickletype for start and finish instead of FKs?
    start = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    end = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)
    stations = db.relationship("StationLink", back_populates="link")
   # vehicle =   db.Column(db.Integer, db.ForeignKey("vehicle.id"))
    def getAllLinks():
        query = Link.query.all()

        links = []
        for link in query:
            names = []
            names.append([Station.query.filter_by(id=link.start).first(), Station.query.filter_by(id=link.end).first()])
            links.append (f"{link.id} {names[0][0].name}-{names[0][1].name}")
        return links
class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(256))
    owner = db.Column(db.Integer, db.ForeignKey("users.id"))
    current_station = db.Column(db.Integer, db.ForeignKey("station.id"))
