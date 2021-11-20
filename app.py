from dpmb.models import db, User
from dpmb.forms import LoginForm, RegisterForm
from flask import render_template, flash, request, redirect
from dpmb import app

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/customer')
def customer_page():
    user = User.query.all()
    return render_template('customer.html', customers=user)

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print("hello")
            reg = User()
            reg.first_name = form.first_name.data
            reg.last_name = form.last_name.data
            reg.email = form.email.data
            reg.password = form.password1.data
            reg.type = "user"
            db.session.add(reg)
            db.session.commit()
            return redirect("/login")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
