from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, SelectField, IntegerField
from wtforms import DateTimeLocalField
from wtforms.fields.simple import HiddenField
from dpmb.models import User, Vehicle, Station, Link, Role, StationLink

class RegisterForm(FlaskForm):
    link_id = HiddenField()
    first_name = StringField(label='First name:', validators=[validators.InputRequired()])
    last_name = StringField(label='Last Name:', validators=[validators.InputRequired()])
    email = StringField(label='Email:', validators=[
        validators.InputRequired(),
        validators.Email(message="Please select a valid email address")])
    password1 = PasswordField(label='Password:', validators=[validators.InputRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[
        validators.InputRequired(),
        validators.EqualTo("password1", message="Passwords don't match")])
    submit = SubmitField(label='Create Account:', validators=[validators.InputRequired()])

class EditForm(RegisterForm):
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm password:', validators=[
        validators.EqualTo("Password1", message="Passwords don't match")])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])

class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[validators.InputRequired()])
    password = PasswordField(label='Password:', validators=[])
    submit = SubmitField(label='Sign In')

class StationForm(FlaskForm):
    id = HiddenField()
    name = StringField(label='Station:', validators=[validators.InputRequired()])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName, validators=[validators.InputRequired()])

class LinkForm(FlaskForm):
    id = HiddenField()
    start = SelectField(u'Start: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    end = SelectField(u'End: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    time_first = DateTimeLocalField('First Station Time', format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    time_last = DateTimeLocalField('Last Station Time', format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    staff = SelectField(u'Staff: ', choices=User.getAllStaffNames, validators=[validators.InputRequired()])
    carrierStaff = SelectField(u'Staff: ', choices=Link.getAllOwnersStaff, validators=[validators.InputRequired()])
    vehicle = SelectField(u'Vehicle: ', choices=Vehicle.getAllVehicles, validators=[validators.InputRequired()])
    carrierVehicle = SelectField(u'Vehicle: ', choices=Link.getAllOwnersVehicles, validators=[validators.InputRequired()])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])

class VehicleForm(FlaskForm):
    id = HiddenField()
    vehicle_name = StringField(label='Vehicle Name: ', validators=[validators.InputRequired()])
    current_station = SelectField(u'Current Station: ', choices=Station.getAllStationNames, validators=[validators.InputRequired()])
    capacity = IntegerField(u'Capacity: ', validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName, validators=[validators.InputRequired()])
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class TicketForm(FlaskForm):
    id = HiddenField()
    email = SelectField(u'User: ', choices=User.getAllEmails, validators=[validators.InputRequired()])
    link = SelectField(u'Link: ', choices=Link.getAllLinks, validators=[validators.InputRequired()])
    expiration = DateTimeLocalField('Expiration Date', format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class UserForm(FlaskForm):
    id = HiddenField()
    first_name = StringField(label='First Name: ', validators=[validators.InputRequired()])
    last_name = StringField(label='Last Name: ', validators=[validators.InputRequired()])
    email = StringField(label='Email: ', validators=[validators.InputRequired()])
    password = PasswordField(label='Password:', validators=[])
    role = SelectField(u'Role: ', choices=Role.getAllRoles, validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName, validators=[validators.InputRequired()])
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class SearchForm(FlaskForm):
    start = SelectField(u'Start station: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    end = SelectField(u'End station: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    time_first = DateTimeLocalField('Choose department time:', format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    submit = SubmitField(label='Search for links', validators=[validators.InputRequired()])
