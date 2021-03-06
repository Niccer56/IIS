from flask_login.utils import logout_user
from dpmb.models import TicketPrice, db, User, Role, Ticket, Link, Station, Vehicle, StationLink
from dpmb.forms import LinkForm, LoginForm, RegisterForm, VehicleForm, SearchForm, StationForm, TicketForm, UserForm
from flask import render_template, flash, request, redirect
from dpmb import app, login_manager, authorize
from flask_login import login_user, login_required, current_user
from dpmb import bcrypt
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route('/')
@app.route('/home')
def home_page():
    form = SearchForm()
    return render_template('home.html', form=form)

@app.route('/home/search', methods=['POST'])
def find_links():
    form = SearchForm()
    if request.method == 'POST':
        stationlinks = []
        times = []
        start_station = StationLink.query.filter_by(station_id=Station.query.filter_by(name=form.start.data).first().id).all()
        end_station = StationLink.query.filter_by(station_id=Station.query.filter_by(name=form.end.data).first().id).all()

        for x in start_station:
            for y in end_station:
                if x.link_id == y.link_id and x not in stationlinks and x.time < y.time and x.time >= form.time_first.data:
                    stationlinks.append([x, x.time, y.time])

        display_content = [form.start.data, form.end.data]
        remaining_tickets = []
        for stationlink in stationlinks:
            link = Link.query.filter_by(id=stationlink[0].link_id).first()
            tickets = Ticket.query.filter_by(linkid=link.id).all()
            capacity = Vehicle.query.filter_by(id=link.vehicle).first().capacity
            if len(tickets) > 0:
                capacity = capacity - len(tickets)
            remaining_tickets.append(capacity)

        print(remaining_tickets)
        return render_template('searched_links.html', links=stationlinks, display_content=display_content, times=times, remaining_tickets=remaining_tickets)

    return redirect("/home")

@app.route('/buy/<int:id>', methods=['POST', 'GET'])
def buy_tickets(id):
    print(id)
    ticket_type = TicketPrice.query.all()

    return render_template('buy_tickets.html', link_id = id, ticket_type = ticket_type)

@app.route('/buy/check', methods=['POST'])
def check_tickets():
    if request.method == 'POST':
        id = request.form.get('id')
        time_last = Link.query.filter_by(id=id).first().time_last
        a_zip = zip(request.form.getlist('email[]'), request.form.getlist('types[]'))
        zipped_tickets = list(a_zip)
        for pair in zipped_tickets:
            email, type = pair
            data = Ticket()
            data.email = email
            data.linkid = id
            data.type_id = TicketPrice.query.filter_by(type=type).first().id
            data.expiration = time_last
            data.paid = False
            data.price = TicketPrice.query.filter_by(type=type).first().price
            db.session.add(data)

        db.session.commit()

    if authorize.has_role("admin", "carrier", "staff", "user"):
        return redirect("/home")
    return redirect("/register")

@app.route('/yourTickets', methods=['GET', 'POST'])
@login_required
def yourTickets_page():
    query = Ticket.query.all()
    tickets = []
    for ticket in query:
        if (ticket.email == current_user.email):
            link = Link.query.filter_by(id=ticket.linkid).first()
            start_station = Station.query.filter_by(id=link.start).first()
            end_station = Station.query.filter_by(id=link.end).first()
            tickets.append([ticket, ticket.email, start_station, end_station, link])

    return render_template('yourTickets.html', tickets=tickets)

@app.route('/customer', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier")
def customer_page():
    roles = Role.query.all()
    types = []
    if (authorize.has_role("admin")):
        form = UserForm()
        user = User.query.all()
        for role in roles:
            types.append(role.name)

        return render_template('customer.html', customers=user, usertype=types, form=form)
    elif (authorize.has_role("carrier")):
        form = UserForm()
        user = User.query.join(User.roles).filter_by(name="staff").all()
        staffList = []
        for staff in user:
            if (current_user.id == staff.owner):
                staffList.append(staff)
                for role in roles:
                    types.append(role.name)

        return render_template('customer.html', customers=staffList, usertype=types, form=form)

@app.route('/ticket', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "staff")
def ticket_page():
    form = TicketForm()
    query = Ticket.query.all()
    tickets = []
    if (authorize.has_role("admin")):
        for ticket in query:
            link = Link.query.filter_by(id=ticket.linkid).first()
            type = TicketPrice.query.filter_by(id=ticket.type_id).first()
            start_station = Station.query.filter_by(id=link.start).first()
            end_station = Station.query.filter_by(id=link.end).first()

            tickets.append([ticket, ticket.email, start_station, end_station, link, type])
        return render_template('ticket.html', tickets=tickets, form=form)

    if (authorize.has_role("staff")):
        for ticket in query:
            link = Link.query.filter_by(id=ticket.linkid).first()
            if (link.staff == current_user.id):
                start_station = Station.query.filter_by(id=link.start).first()
                end_station = Station.query.filter_by(id=link.end).first()
                type = TicketPrice.query.filter_by(id=ticket.type_id).first()

                tickets.append([ticket, ticket.email, start_station, end_station, link, type])
        return render_template('ticket.html', tickets=tickets, form=form)

@app.route('/vehicle', methods=['GET'])
@login_required
@authorize.has_role("admin", "carrier")
def vehicle_page():
    form = VehicleForm()
    vehicle = Vehicle.query.all()
    vehicles = []
    if (authorize.has_role("admin")):
        for current in vehicle:
            query_station = Station.query.filter_by(id=current.current_station).first().name
            query_carrier = User.query.filter_by(id=current.owner).first().email
            vehicles.append([current, query_station, query_carrier])

        return render_template('vehicle.html', vehicles=vehicles, form=form)
    elif (authorize.has_role("carrier")):
        for current in vehicle:
            if (current_user.id == current.owner):
                query_station = Station.query.filter_by(id=current.current_station).first().name
                query_carrier = User.query.filter_by(id=current.owner).first().email
                vehicles.append([current, query_station, query_carrier])

        return render_template('vehicle.html', vehicles=vehicles, form=form)

@app.route('/station', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier")
def station_page():
    form = StationForm()
    station = Station.query.all()
    if (authorize.has_role("admin")):
        return render_template('station.html', stations=station, form=form)
    elif (authorize.has_role("carrier")):
        ownStations = []
        for current in station:
            if (current_user.id == current.owner):
                ownStations.append(current)
        return render_template('station.html', stations=ownStations, form=form)

@app.route('/link', methods=['GET', 'POST'])
@login_required
@authorize.has_role("admin", "carrier")
def link_page():
    query = Link.query.all()
    form = LinkForm()
    names = []
    if (authorize.has_role("admin")):
        for link in query:
            links = []
            links.append([Station.query.filter_by(id=link.start).first(), Station.query.filter_by(id=link.end).first()])
            for station in links:
                staff = User.query.filter_by(id=link.staff).first()
                tickets = Ticket.query.filter_by(linkid=link.id).all()
                capacity = Vehicle.query.filter_by(id=link.vehicle).first().capacity
                if len(tickets) > 0:
                    capacity = capacity - len(tickets)
                names.append([station[0].name + " " + link.time_first.strftime("%m/%d/%Y, %H:%M"), station[1].name + " " + link.time_last.strftime("%m/%d/%Y, %H:%M"), link.id, staff.email, capacity])
        return render_template('link.html', links=names, form=form)
    if (authorize.has_role("carrier")):
        for link in query:
            staff = User.query.filter_by(id=link.staff).first()
            if (staff.owner == current_user.id):
                links = []
                links.append([Station.query.filter_by(id=link.start).first(), Station.query.filter_by(id=link.end).first()])
                for station in links:
                    tickets = Ticket.query.filter_by(linkid=link.id).all()
                    capacity = Vehicle.query.filter_by(id=link.vehicle).first().capacity
                    if len(tickets) > 0:
                        capacity = capacity - len(tickets)
                    names.append([station[0].name + " " + link.time_first.strftime("%m/%d/%Y, %H:%M"), station[1].name + " " + link.time_last.strftime("%m/%d/%Y, %H:%M"), link.id, staff.email, capacity])
        return render_template('link.html', links=names, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if authorize.has_role("admin", "carrier", "staff", "user"):
        return redirect("/home")
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
@login_required
def logout_page():
    logout_user()
    flash('You have been successfuly logged out!')
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
            reg.owner = 0
            role = Role.query.filter_by(name="user").first()
            reg.roles = [role]
            db.session.add(reg)
            db.session.commit()
            return redirect("/login")
        else:
            for err in form.errors:
                flash(form.errors[err][0])
    return render_template('register.html', form=form)

@app.route('/station/edit_station/<int:id>', methods=['POST', 'GET'])
@login_required
@authorize.has_role("admin", "carrier")
def stations_form(id):
    link = Link.query.filter_by(id=id).first()
    stations = Station.query.all()
    return render_template('edit_stations.html', stations=stations, link=link)

@app.route('/station/edit_station/<string:type>', methods=['POST'])
@login_required
@authorize.has_role("admin", "carrier")
def edit_station(type):
    form = StationForm()
    if request.method == 'POST':
        if type == "add":
            data = Station()
            if (authorize.has_role("admin")):
                data.owner = User.query.filter_by(email=form.owner.data).first().id
                data.verified = True
            elif (authorize.has_role("carrier")):
                data.owner = current_user.id
                data.verified = False
            data.name = form.name.data.strip()
            db.session.add(data)
            db.session.commit()
        elif type == "edit":

            toedit = Station.query.filter_by(id=form.id.data).first()
            if (authorize.has_role("admin")):
                toedit.owner = User.query.filter_by(email=form.owner.data).first().id
            elif (authorize.has_role("carrier")):
                toedit.owner = current_user.id
                toedit.verified = False
            toedit.name = form.name.data.strip()
            db.session.commit()
        elif type == "delete":
            station = Station.query.filter_by(id=form.id.data).first()
            links = Link.query.filter_by(start=station.id).all()
            if len(links) > 0:
                for link in links:
                    tickets = Ticket.query.filter_by(linkid=link.id).all()
                    if len(tickets) > 0:
                        for ticket in tickets:
                            db.session.delete(ticket)
            if len(links) > 0:
                for link in links:
                    db.session.delete(link)
            links = Link.query.filter_by(end=station.id).all()
            if len(links) > 0:
                for link in links:
                    tickets = Ticket.query.filter_by(linkid=link.id).all()
                    if len(tickets) > 0:
                        for ticket in tickets:
                            db.session.delete(ticket)
            if len(links) > 0:
                for link in links:
                    db.session.delete(link)
            if station is not None:
                db.session.delete(station)
                db.session.commit()

    return redirect("/station")

@app.route('/station/approve/<int:id>', methods=['POST', 'GET'])
@login_required
@authorize.has_role("admin")
def approve_station(id):
    toedit = Station.query.filter_by(id=id).first()
    toedit.verified = True
    db.session.commit()
    return redirect("/station")

@app.route('/customer/edit_customer/<string:type>', methods=['POST'])
@login_required
@authorize.has_role("admin", "carrier")
def edit_customer(type):
    form = UserForm()
    if request.method == 'POST':
        if type == "add":
            if len(User.query.filter_by(email=form.email.data.strip()).all()) > 0:
                flash(f"User with email {form.email.data.strip()} already exists.")
                return redirect("/customer")
            data = User()
            data.first_name = form.first_name.data.strip()
            data.last_name = form.last_name.data.strip()
            data.email = form.email.data.strip()
            data.password = bcrypt.generate_password_hash(form.password.data)
            if (authorize.has_role("admin")):
                role = Role.query.filter_by(name=form.role.data).first()
                data.owner = User.query.filter_by(email=form.owner.data).first().id
            elif (authorize.has_role("carrier")):
                role = Role.query.filter_by(name="staff").first()
                data.owner = current_user.id
            data.roles = [role]
            db.session.add(data)
            db.session.commit()
        elif type == "edit":
            toedit = User.query.filter_by(id=form.id.data).first()
            if form.email.data.strip() != toedit.email:
                if len(User.query.filter_by(email=form.email.data.strip()).all()) > 0:
                    flash(f"User with email {form.email.data.strip()} already exists.")
                    return redirect("/customer")
            if (authorize.has_role("carrier")):
                role = Role.query.filter_by(name="staff").first()
            elif (authorize.has_role("admin")):
                role = Role.query.filter_by(name=form.role.data).first()
                toedit.owner = User.query.filter_by(email=form.owner.data).first().id
            toedit.first_name = form.first_name.data
            toedit.last_name = form.last_name.data
            toedit.email = form.email.data
            if form.password.data:
                toedit.password = bcrypt.generate_password_hash(form.password.data)
            toedit.roles = [role]
            db.session.commit()
        elif type == "delete":
            user = User.query.filter_by(id=form.id.data).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()

    return redirect("/customer")

@app.route('/ticket/pay/<int:id>', methods=['GET']) 
@login_required
@authorize.has_role("admin", "staff")
def pay_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    ticket.paid = True
    db.session.commit()
    return redirect('/ticket')

@app.route('/myticket/pay/<int:id>', methods=['GET']) 
@login_required
def pay_myticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    ticket.paid = True
    db.session.commit()
    return redirect('/yourTickets')

@app.route('/ticket/edit_ticket/<string:type>', methods=['POST'])
@login_required
@authorize.has_role("admin", "staff")
def edit_ticket(type):
    form = TicketForm()
    if request.method == 'POST':
        if type == "add":
            data = Ticket()
            if (authorize.has_role("admin")):
                link = form.link.data.partition(" ")[0]
            elif (authorize.has_role("staff")):
                link = form.staffLink.data.partition(" ")[0]
            data.email = form.email.data
            data.linkid = link
            data.type_id = TicketPrice.query.filter_by(type=form.type.data).first().id
            data.expiration = form.expiration.data.strftime("%Y-%m-%dT%H:%M")
            data.price = TicketPrice.query.filter_by(type=form.type.data).first().price
            data.paid = False
            db.session.add(data)
            db.session.commit()
        elif type == "edit":
            toedit = Ticket.query.filter_by(id=form.id.data).first()
            if (authorize.has_role("admin")):
                link = form.link.data.partition(" ")[0]
            elif (authorize.has_role("staff")):
                link = form.staffLink.data.partition(" ")[0]
            toedit.email = form.email.data
            toedit.linkid = link
            toedit.type_id = TicketPrice.query.filter_by(type=form.type.data).first().id
            toedit.price = TicketPrice.query.filter_by(type=form.type.data).first().price
            toedit.expiration = form.expiration.data.strftime("%Y-%m-%dT%H:%M")
            db.session.commit()
        elif type == "delete":
            ticket = Ticket.query.filter_by(id=form.id.data).first()
            if ticket is not None:
                db.session.delete(ticket)
                db.session.commit()

    return redirect("/ticket")

@app.route('/link/edit_link/<string:type>', methods=['POST'])
@login_required
@authorize.has_role("admin", "carrier")
def edit_link(type):
    form = LinkForm()
    if request.method == 'POST':
        if type == "add":
            data = Link()
            stationlink_first = StationLink()
            stationlink_last = StationLink()

            name = form.start.data.partition(" ")[0]
            station = Station.query.filter_by(name=name).first()
            data.start = station.id
            stationlink_first.station = station
            stationlink_first.time = form.time_first.data

            nameend = form.end.data.partition(" ")[0]
            station = Station.query.filter_by(name=nameend).first()
            data.end = station.id
            data.time_first = form.time_first.data
            data.time_last = form.time_last.data
            stationlink_last.station = station
            stationlink_last.time = form.time_last.data

            if name == nameend:
                flash("Same station selected as start and end.")
                return redirect("/link")
            if data.time_first > data.time_last:
                flash("Start station's time can't be lower than end station's time")
                return redirect("/link")

            if (authorize.has_role("admin")):
                data.staff = User.query.filter_by(email=form.staff.data).first().id
                data.vehicle = Vehicle.query.filter_by(vehicle_name=form.vehicle.data).first().id
            elif (authorize.has_role("carrier")):
                data.staff = User.query.filter_by(email=form.carrierStaff.data).first().id
                data.vehicle = Vehicle.query.filter_by(vehicle_name=form.carrierVehicle.data).first().id

            data.stations.append(stationlink_first)
            data.stations.append(stationlink_last)
            db.session.add(data)
            db.session.commit()
        elif type == "edit":
            toedit = Link.query.filter_by(id=form.id.data).first()

            for x in toedit.stations:
                if form.time_first.data > x.time and x.station_id != toedit.start:
                    flash("Selected times are in colision with link's station times")
                    return redirect("/link")
                if form.time_last.data < x.time and x.station_id != toedit.end:
                    flash("Selected times are in colision with link's station times")
                    return redirect("/link")

            sorted_stations = StationLink.query.filter_by(link_id=form.id.data).all()
            sorted_stations.sort(key=lambda x: x.time)
            toedit_station1 = sorted_stations[0]
            toedit_station2 = sorted_stations[-1]
            name = form.start.data.partition(" ")[0]
            station = Station.query.filter_by(name=name).first()
            if len(StationLink.query.filter_by(link_id=form.id.data, station_id=station.id).all()) > 0:
                if station.id != toedit.start:
                    flash("Station is already used in this link.")
                    return redirect("/link")
            toedit.start = station.id

            nameend = form.end.data.partition(" ")[0]
            station = Station.query.filter_by(name=nameend).first()
            if len(StationLink.query.filter_by(link_id=form.id.data, station_id=station.id).all()) > 0:
                if station.id != toedit.end:
                    flash("Station is already used in this link.")
                    return redirect("/link")
            toedit.end = station.id

            if name == nameend:
                flash("Same station selected as start and end.")
                return redirect("/link")

            if (authorize.has_role("admin")):
                toedit.staff = User.query.filter_by(email=form.staff.data).first().id
                toedit.vehicle = Vehicle.query.filter_by(vehicle_name=form.vehicle.data).first().id
            elif (authorize.has_role("carrier")):
                toedit.staff = User.query.filter_by(email=form.carrierStaff.data).first().id
                toedit.vehicle = Vehicle.query.filter_by(vehicle_name=form.carrierVehicle.data).first().id
            toedit.time_first = form.time_first.data
            toedit_station1.time = form.time_first.data
            toedit_station2.time = form.time_last.data
            station = Station.query.filter_by(name=name).first()
            toedit_station1.station_id = station.id
            station = Station.query.filter_by(name=nameend).first()
            toedit_station2.station_id = station.id
            toedit.time_last = form.time_last.data

            db.session.commit()
        elif type == "delete":
            link = Link.query.filter_by(id=form.id.data).first()
            tickets = Ticket.query.filter_by(linkid=link.id).all()
            if len(tickets) > 0:
                for ticket in tickets:
                    db.session.delete(ticket)
            if link is not None:
                db.session.delete(link)
                db.session.commit()
        elif type == "stations":
            id = request.form.get('id')
            link = Link.query.filter_by(id=id).first()
            temp = []
            a_zip = zip(request.form.getlist('station[]'), request.form.getlist('station_time[]'))
            zipped_stations = list(a_zip)
            for pair in zipped_stations:
                station_id, time = pair
                time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
                if station_id == "--Choose Station--":
                    flash("Station has been left unselected")
                    return redirect(f"/station/edit_station/{id}")
                if station_id == link.start or station_id == link.end:
                    flash("Selected station is already used as start or end station.")
                    return redirect(f"/station/edit_station/{id}")
                if time < link.time_first or time > link.time_last:
                    flash(f"Selected station time {time} is out of the link's time range.")
                    return redirect(f"/station/edit_station/{id}")

                station_link = StationLink(time=time)
                station_link.station = Station.query.filter_by(id=station_id).first()
                temp.append(station_link)

            for slink in link.stations:
                if slink.station_id != link.start and slink.station_id != link.end:
                    db.session.delete(slink)

            for slink in temp:
                link.stations.append(slink)
            db.session.commit()

    return redirect("/link")

@app.route('/vehicle/edit_vehicle/<string:type>', methods=['POST'])
@login_required
@authorize.has_role("admin", "carrier")
def edit_vehicle(type):
    form = VehicleForm()
    if request.method == 'POST':
        if type == "add":
            data = Vehicle()
            data.vehicle_name = form.vehicle_name.data.strip()
            if (authorize.has_role("admin")):
                data.owner = User.query.filter_by(email=form.owner.data).first().id
            elif (authorize.has_role("carrier")):
                data.owner = current_user.id
            data.current_station = Station.query.filter_by(name=form.current_station.data).first().id
            data.capacity = form.capacity.data
            db.session.add(data)
            db.session.commit()
        elif type == "edit":
            toedit = Vehicle.query.filter_by(id=form.id.data).first()
            toedit.vehicle_name = form.vehicle_name.data
            if (authorize.has_role("admin")):
                toedit.owner = User.query.filter_by(email=form.owner.data).first().id
            toedit.current_station = Station.query.filter_by(name=form.current_station.data).first().id
            toedit.capacity = form.capacity.data
            db.session.commit()
        elif type == "delete":
            vehicle = Vehicle.query.filter_by(id=form.id.data).first()
            if vehicle is not None:
                db.session.delete(vehicle)
                db.session.commit()

    return redirect("/vehicle")


if __name__ == '__main__':
    app.run(debug=True)
