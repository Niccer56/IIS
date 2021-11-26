from flask_login.utils import logout_user
from dpmb.models import db, User, Role, Ticket, Link, Station, Vehicle, StationLink
from dpmb.forms import LoginForm, RegisterForm, EditForm, VehicleForm, StationForm, TicketForm, UserForm
from flask import render_template, flash, request, redirect
from dpmb import app, login_manager, authorize
from flask_login import login_user, login_required
from dpmb import bcrypt
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
#@login_required
#@authorize.has_role("admin")
def customer_page():
    #User.query.join(User.roles).filter_by(name="carrier").all()
    form = UserForm()
    user = User.query.all()
    roles = Role.query.all()
    types = []
    for role in roles:
        types.append(role.name)

    return render_template('customer.html', customers=user, usertype=types, form = form)

@app.route('/ticket', methods=['GET', 'POST'])
#@login_required
#@authorize.has_role("admin", "staff")
def ticket_page():
    form = TicketForm()
    query = Ticket.query.all()
    tickets = []
    for ticket in query:
        link = Link.query.filter_by(id=ticket.linkid).first()
        tickets.append([ticket, User.query.filter_by(id=ticket.customerid).first(), Station.query.filter_by(id=link.start).first(), Station.query.filter_by(id=link.end).first(), link])
    return render_template('ticket.html', tickets=tickets, form=form)

@app.route('/vehicle', methods=['GET'])
#@login_required
#@authorize.has_role("admin", "carrier")
def vehicle_page():
    form = VehicleForm()
    vehicle = Vehicle.query.all()
    return render_template('vehicle.html', vehicles=vehicle, form=form)

@app.route('/station', methods=['GET', 'POST'])
#@login_required
#@authorize.has_role("admin", "carrier")
def station_page():
    form = StationForm()
    station = Station.query.all()
    return render_template('station.html', stations=station, form=form)

@app.route('/link', methods=['GET', 'POST'])
#@login_required
#@authorize.has_role("admin", "carrier")
def link_page():

    query = Link.query.all()
    links = []
    for link in query:
        links.append([link, Station.query.filter_by(id=link.start).first(), Station.query.filter_by(id=link.end).first()])
    stations = Station.query.all()
    return render_template('link.html', links=links, stations=stations)

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
    flash('You have been successfuly logged out !')
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







@app.route('/link/delete/<int:id>')
def delete_link(id):
    link = Link.query.filter_by(id=id).first()
    if link is not None:
        db.session.delete(link)
        db.session.commit()
    return redirect("/link")



@app.route('/customer/changestart/<int:id>', methods=["POST"])
def change_start(id):
    link = Link.query.filter_by(id=id).first()
    if link is not None:
        start = request.form.get("start")
        station = Station.query.filter_by(name=start).first()
        link.start = station.id
        db.session.commit()
    return redirect("/link")

@app.route('/customer/changefinish/<int:id>', methods=["POST"])
def change_end(id):
    link = Link.query.filter_by(id=id).first()
    if link is not None:
        end = request.form.get("end")
        station = Station.query.filter_by(name=end).first()
        link.end = station.id
        db.session.commit()
    return redirect("/link")

"""@app.route('/customer/edit/<int:id>', methods=["GET", "POST"])
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
    return render_template('edit.html', form=form, username=user.first_name)"""

@app.route('/station/edit_station/<string:type>', methods=['POST'])
def edit_station(type):
    form = StationForm()
    if request.method == 'POST':
        if type == "add":
            data = Station()

            data.name = form.name.data.strip()
            db.session.add(data)
            db.session.commit()
            return redirect("/station")
        elif type == "edit":

            toedit = Station.query.filter_by(id=form.id.data).first()
            toedit.name = form.name.data
            db.session.commit()
            return redirect("/station")
        elif type == "delete":
            station = Station.query.filter_by(id=form.id.data).first()
            if station is not None:
                db.session.delete(station)
                db.session.commit()
                return redirect("/station")

@app.route('/customer/edit_customer/<string:type>', methods=['POST'])
def edit_customer(type):
    form = UserForm()
    if request.method == 'POST':
        if type == "add":
            data = User()
            data.first_name = form.first_name.data.strip()
            data.last_name = form.last_name.data.strip()
            data.email = form.email.data.strip()
            data.password = form.password.data
            role = Role.query.filter_by(name=form.role.data).first()
            data.roles = [role]
            db.session.add(data)
            db.session.commit()
            return redirect("/customer")
        elif type == "edit":
            role = Role.query.filter_by(name=form.role.data).first()
            toedit = User.query.filter_by(id=form.id.data).first()
            toedit.first_name = form.first_name.data
            toedit.last_name = form.last_name.data
            toedit.email = form.email.data
            toedit.password = form.password.data
            toedit.roles = [role]
            db.session.commit()
            return redirect("/customer")
        elif type == "delete":
            user = User.query.filter_by(id=form.id.data).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
                return redirect("/customer")

@app.route('/ticket/edit_ticket/<string:type>', methods=['POST'])
def edit_ticket(type):
    form = TicketForm()
    if request.method == 'POST':
        if type == "add":
            data = Ticket()
            user = User.query.filter_by(email=form.email.data).first()
            link = form.link.data.partition(" ")[0]
            data.customerid = user.id
            data.linkid = link
            data.expiration = form.expiration.data
            db.session.add(data)
            db.session.commit()
            return redirect("/ticket")
        elif type == "edit":
            toedit = Ticket.query.filter_by(id=form.id.data).first()
            user = User.query.filter_by(email=form.email.data).first()
            link = form.link.data.partition(" ")[0]
            toedit.customerid = user.id
            toedit.linkid = link
            toedit.expiration = form.expiration.data
            db.session.commit()
            return redirect("/ticket")
        elif type == "delete":
            ticket = Ticket.query.filter_by(id=form.id.data).first()
            if ticket is not None:
                db.session.delete(ticket)
                db.session.commit()
                return redirect("/ticket")


@app.route('/vehicle/edit_vehicle/<string:type>', methods=['POST'])
def edit_vehicle(type):
    form = VehicleForm()
    if request.method == 'POST':
        if type == "add":
            data = Vehicle()
            data.vehicle_name = form.vehicle_name.data.strip()
            db.session.add(data)
            db.session.commit()
            return redirect("/vehicle")
        elif type == "edit":

            toedit = Vehicle.query.filter_by(id=form.id.data).first()
            toedit.vehicle_name = form.vehicle_name.data
            db.session.commit()
            return redirect("/vehicle")
        elif type == "delete":
            vehicle = Vehicle.query.filter_by(id=form.id.data).first()
            if vehicle is not None:
                db.session.delete(vehicle)
                db.session.commit()
                return redirect("/vehicle")


if __name__ == '__main__':
    app.run(debug=True)
