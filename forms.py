from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    first_name = StringField(label='Meno:')
    last_name = StringField(label='Priezivko:')
    email = StringField(label='Email:')
    password1 = PasswordField(label='Heslo:')
    password2 = PasswordField(label='Potvrďte heslo:')
    submit = SubmitField(label='Vytvoriť účet:')

class LoginForm(FlaskForm):
    first_name = StringField(label='Meno:')
    last_name = StringField(label='Priezivko:')
    password1 = PasswordField(label='Heslo:')
    submit = SubmitField(label='Prihlásiť sa:')