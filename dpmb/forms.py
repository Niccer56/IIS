from flask_admin.contrib.sqla.view import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, SelectField, DateField, FieldList, FormField
from wtforms import DateTimeLocalField
from wtforms.fields.simple import HiddenField
from dpmb.models import User, Vehicle, Station, Link, Role, StationLink
class RegisterForm(FlaskForm):

    first_name = StringField(label='Meno:', validators=[validators.InputRequired()])
    last_name = StringField(label='Priezivko:', validators=[validators.InputRequired()])
    email = StringField(label='Email:', validators=[
        validators.InputRequired(),
        validators.Email(message="Please select a valid email address")])
    password1 = PasswordField(label='Heslo:', validators=[validators.InputRequired()])
    password2 = PasswordField(label='Potvrďte heslo:', validators=[
        validators.InputRequired(),
        validators.EqualTo("password1", message="Passwords don't match")])
    submit = SubmitField(label='Vytvoriť účet:', validators=[validators.InputRequired()])

class EditForm(RegisterForm):
    password1 = PasswordField(label='Heslo:')
    password2 = PasswordField(label='Potvrďte heslo:', validators=[
        validators.EqualTo("password1", message="Passwords don't match")])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])

class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[validators.InputRequired()])
    password = PasswordField(label='Password:', validators=[])
    submit = SubmitField(label='Sign In')

class StationForm(FlaskForm):
    id = HiddenField()
    name = StringField(label='Zastávka:', validators=[validators.InputRequired()])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName , validators=[validators.InputRequired()])
class LinkForm(FlaskForm):
    id = HiddenField()
    start = SelectField(u'Start: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    end = SelectField(u'End: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    time_first =DateTimeLocalField('First Station Time',format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    time_last = DateTimeLocalField('Last Station Time',format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])

class CurrentStation(FlaskForm):
    station = SelectField(u'Current Station: ', choices=Station.getAllStationNames, validators=[validators.InputRequired()])
    time = DateTimeLocalField('First Station Time',format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])

class LinkStationForm(FlaskForm):
    stations = FieldList(FormField(CurrentStation),min_entries=2)
    submit = SubmitField(label='Save Stations', validators=[validators.InputRequired()])

class VehicleForm(FlaskForm):
    id = HiddenField()
    vehicle_name = StringField(label='Vehicle Name: ', validators=[validators.InputRequired()])
    current_station = SelectField(u'Current Station: ', choices=Station.getAllStationNames, validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName , validators=[validators.InputRequired()])
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class TicketForm(FlaskForm):
    id = HiddenField()
    email = SelectField(u'User: ', choices=User.getAllEmails, validators=[validators.InputRequired()]) 
    link = SelectField(u'Link: ', choices=Link.getAllLinks, validators=[validators.InputRequired()])
    expiration = DateTimeLocalField('Expiration Date',format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])    # bude treba este format casu upravit
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class UserForm(FlaskForm):
    id = HiddenField()
    first_name = StringField(label='First Name: ', validators=[validators.InputRequired()])
    last_name = StringField(label='Last Name: ', validators=[validators.InputRequired()])
    email = StringField(label='Email: ', validators=[validators.InputRequired()])
    password = PasswordField(label='Password:', validators=[])  
    role = SelectField(u'Role: ', choices=Role.getAllRoles, validators=[validators.InputRequired()])
    owner = SelectField(u'Owner: ', choices=User.getAllCarriersName , validators=[validators.InputRequired()])
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])

class SearchForm(FlaskForm):
    start = SelectField(u'Start station: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    end = SelectField(u'End station: ', choices=StationLink.getAllStations, validators=[validators.InputRequired()])
    time_first =DateTimeLocalField('Choose department time:',format='%Y-%m-%dT%H:%M', validators=[validators.InputRequired()])
    submit = SubmitField(label='Search for links', validators=[validators.InputRequired()])

    

