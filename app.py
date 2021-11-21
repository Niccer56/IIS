from dpmb.models import db, User, UserType
from dpmb.forms import LoginForm, RegisterForm, EditForm
from flask import render_template, flash, request, redirect
from dpmb import app, login_manager
from flask_login import login_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/customer')
def customer_page():
    user = User.query.all()
    return render_template('customer.html', customers=user, usertype=UserType)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.strip(), password=form.password.data).first()
            if not user:
                flash("Invalid login credentials")
                return render_template('login.html', form=form)
            login_user(user)
            return redirect("/home")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if len(User.query.filter_by(email=form.email.data).all()) != 0:
                flash("This email adress is already in use.")
                return render_template('register.html', form=form)
            reg = User()
            reg.first_name = form.first_name.data.strip()
            reg.last_name = form.last_name.data.strip()
            reg.email = form.email.data.strip()
            reg.password = form.password1.data
            reg.type = "user"
            db.session.add(reg)
            db.session.commit()
            return redirect("/login")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('register.html', form=form)

@app.route('/customer/delete/<int:id>')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return redirect("/customer")

@app.route('/customer/changetype/<int:id>', methods=["POST"])
def change_type(id):
    user = User.query.filter_by(id=id).first()
    if user is not None:
        user.type = request.form.get("type")
        db.session.commit()
    return redirect("/customer")

@app.route('/customer/edit/<int:id>', methods=["GET", "POST"])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    form = EditForm(obj=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(user)
            if form.password1.data:
                user.password = form.password1.data
            db.session.commit()
            return redirect("/customer")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('edit.html', form=form, username=user.first_name)


if __name__ == '__main__':
    app.run(debug=True)
