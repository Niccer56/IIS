from dpmb.models import db, Customer
from dpmb.forms import LoginForm, RegisterForm
from flask import Flask, render_template
from dpmb import app, db
import os

@app.route('/')
@app.route('/home')
def home_page():
    
    return render_template('home.html')


@app.route('/customer')
def customer_page():
    customer = Customer.query.all()
    return render_template('customer.html',customers=customer)

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.is_submitted():
        reg = Customer()
        reg.email = form.email.data
        reg.username = form.first_name.data
        db.session.add(reg)
        db.session.commit()
        
        #add_customer(mysql, form.first_name.data, form.last_name.data, form.email.data, form.password1.data)
        
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

