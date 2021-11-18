from .db_models import add_customer, get_customers
from .forms import LoginForm, RegisterForm
from flask import Flask, render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import os

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'winess.irineva.nyara.network'
app.config['MYSQL_DATABASE_PORT'] = 3360
app.config['MYSQL_DATABASE_USER'] = 'michal'
app.config['MYSQL_DATABASE_PASSWORD'] = 'whiskeyindianovember'
app.config['MYSQL_DATABASE_DB'] = 'IIS'
app.config['SECRET_KEY'] = os.urandom(32) #enable to work with forms
 
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

@app.route('/')
@app.route('/home')
def home_page():
    
    return render_template('home.html')

@app.route('/customer')
def customer_page():
    result=get_customers(mysql)
    return render_template('customer.html',customers=result)

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        print('user_is_ready')
        add_customer(mysql, form.first_name.data, form.last_name.data, form.email.data, form.password1.data)
        
    return render_template('register.html', form=form)
