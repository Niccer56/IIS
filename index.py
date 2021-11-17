from .db_models import get_customers
from flask import Flask, render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'winess.irineva.nyara.network'
app.config['MYSQL_DATABASE_PORT'] = 3360
app.config['MYSQL_DATABASE_USER'] = 'michal'
app.config['MYSQL_DATABASE_PASSWORD'] = 'whiskeyindianovember'
app.config['MYSQL_DATABASE_DB'] = 'IIS'
 
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

@app.route('/')
@app.route('/home')
def home_page():
    #cursor = mysql.get_db().cursor()
    #cursor.execute('''INSERT INTO customer (first_name, last_name) VALUES ('Tom B. en', 'Ska 21')''')
    #mysql.get_db().commit()
    #cursor.execute('''SHOW TABLES''')
    #sql = "SELECT * FROM customer"
    #cursor.execute(sql)
    #result= cursor.fetchall()
    result=get_customers(mysql)
    print(result)
    

    return render_template('home.html')

@app.route('/customer')
def customer_page():
    return render_template('customer.html')