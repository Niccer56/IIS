from flask_authorize.plugin import CURRENT_USER
from flask_login.utils import logout_user
from dpmb.models import db, User, Role, Ticket, Link, Station, Vehicle
from dpmb.forms import LoginForm, RegisterForm, EditForm
from flask import render_template, flash, request, redirect
from dpmb import app, login_manager, authorize
from flask_login import login_user, login_required
from dpmb import bcrypt

        

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin")
def customer_page():
    user = User.query.all()
    roles = Role.query.all()
    types = []
    for role in roles:
        types.append(role.name)
    return render_template('customer.html', customers=user, usertype=types)

@app.route('/ticket', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "staff" )
def ticket_page():
    ticket = Ticket.query.all()
    return render_template('ticket.html', tickets=ticket)

@app.route('/vehicle', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier" )
def vehicle_page():
    vehicle = Vehicle.query.all()
    return render_template('vehicle.html', vehicles=vehicle)    

@app.route('/station', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier" )
def station_page():
    station = Station.query.all()
    return render_template('station.html', stations=station)    

@app.route('/link', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier" )
def link_page():
    link = Link.query.all()
    return render_template('link.html', links=link)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.strip()).first()
            if not user or not user.password_check(form.password.data):
                flash("Invalid login credentials")
                return render_template('login.html', form=form)
            login_user(user)
            return redirect("/home")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash(f'You have been successfuly logged out !')
    return redirect('/login')

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
            reg.password = bcrypt.generate_password_hash(form.password1.data)
            role = Role.query.filter_by(name="user").first()
            reg.roles = [role]
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

@app.route('/station/delete/<int:id>')
def delete_station(id):
    station = Station.query.filter_by(id=id).first()
    if station is not None:
        db.session.delete(station)
        db.session.commit()
    return redirect("/station")        

@app.route('/ticket/delete/<int:id>')
def delete_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    if ticket is not None:
        db.session.delete(ticket)
        db.session.commit()
    return redirect("/ticket")

@app.route('/vehicle/delete/<int:id>')
def delete_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id).first()
    if vehicle is not None:
        db.session.delete(vehicle)
        db.session.commit()
    return redirect("/vehicle")         

@app.route('/link/delete/<int:id>')
def delete_link(id):
    link = Link.query.filter_by(id=id).first()
    if link is not None:
        db.session.delete(link)
        db.session.commit()
    return redirect("/link")      

@app.route('/customer/changetype/<int:id>', methods=["POST"])
def change_type(id):
    user = User.query.filter_by(id=id).first()
    if user is not None:
        type = request.form.get("type")
        role = Role.query.filter_by(name=type).first()
        user.roles = [role]
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
