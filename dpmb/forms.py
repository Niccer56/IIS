from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

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
    password1 = PasswordField(label='Heslo:', validators=[])
    password2 = PasswordField(label='Potvrďte heslo:', validators=[
        validators.EqualTo("password1", message="Passwords don't match")])
    submit = SubmitField(label='Confirm', validators=[validators.InputRequired()])

class LoginForm(FlaskForm):
    first_name = StringField(label='Meno:')
    last_name = StringField(label='Priezivko:')
    password1 = PasswordField(label='Heslo:')
    submit = SubmitField(label='Prihlásiť sa:')
