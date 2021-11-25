from flask_admin.contrib.sqla.view import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, SelectField
from dpmb.models import User, Vehicle, Station
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

class VehicleForm(FlaskForm):

    vehicle_name = StringField(label='Vehicle Name: ', validators=[validators.InputRequired()])
    '''current_station = SelectField(u'Current Station: ',choices=Station.getAllStationNames(), validators=[validators.InputRequired()])'''
    submit = SubmitField(label='Submit', validators=[validators.InputRequired()])





