from flask import Flask, render_template, request, Response, session
import flask
import json
import requests
import functools
import MySQLdb
import datetime
from subprocess import call

app = Flask(__name__)
app.secret_key = 'eskihafiz'
db = MySQLdb.connect(user="root", passwd="kaan", db="airline_company")

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        #session.pop('isloggedin', None)
        if 'isloggedin' in session:
            return method(*args, **kwargs)
        else:
            return flask.redirect('/login')
    return wrapper

def signup_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'signup' in session:
            return method(*args, **kwargs)
        else:
            return flask.redirect('/login')
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    #session.pop('isloggedin', None)
    if 'isloggedin' in session:
        return flask.redirect('/')
    elif 'signup' in session:
        return flask.redirect('/signup')

    if request.method == 'POST':
        if request.form['submit'] == 'Signup':
            session['signup'] = True
            return flask.redirect('/signup')
        if request.form['submit'] == 'Login':
            if 'id' in request.form and 'password' in request.form:
                userid = request.form['id']
                password = request.form['password']
                cursor = db.cursor()
                cursor.execute("SELECT * FROM person WHERE person_id='{}' and password='{}'".format(userid, password))
                data = cursor.fetchone()

                if data == None:
                    return flask.redirect('/login')
                session['id'] = request.form['id']
                session['isloggedin'] = True

                if userid == 0:
                    session['admin'] = True

                cursor.execute("SELECT * FROM passenger WHERE pass_id='{}'".format(userid))
                data = cursor.fetchone()
                if data != None:
                    session['passenger'] = True

                cursor.execute("SELECT * FROM pilot WHERE pilot_id='{}'".format(userid))
                data = cursor.fetchone()
                if data != None:
                    session['pilot'] = True

                cursor.execute("SELECT * FROM flight_attendant WHERE att_id='{}'".format(userid))
                data = cursor.fetchone()
                if data != None:
                    session['attendant'] = True

                cursor.execute("SELECT * FROM store_staff WHERE store_staff_id='{}'".format(userid))
                data = cursor.fetchone()
                if data != None:
                    session['store_staff'] = True

                cursor.execute("SELECT * FROM ticket_staff WHERE ticket_staff_id='{}'".format(userid))
                data = cursor.fetchone()
                if data != None:
                    session['ticket_staff'] = True
                return flask.redirect('/')
            return flask.redirect('/login')
    return render_template('login.html')

@app.route('/signup')
def signup():
    cursor = db.cursor()
    person_name = "Kaan Elgin"
    password = "kaan"
    no = "13"
    street = "62"
    town = "bahceli"
    city = "ankara"
    phone = "123456789"
    email = "kaanelgin@gmail.com"

    cursor.execute("INSERT INTO person(person_name, password, address_no, street, town, city) "
        " VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(person_name, password, no, street, town, city)) 
    cursor.execute("SELECT LAST_INSERT_ID()")
    data = cursor.fetchone()
    cursor.execute("INSERT INTO passenger(pass_id, expenditure, prom_expenditure)"
        " VALUES('{}', 0, 0)".format(data[0]))
    cursor.execute("INSERT INTO person_phone(person_id, phone)"
        " VALUES('{}', '{}')".format(data[0], phone))
    cursor.execute("INSERT INTO person_email(person_id, email)"
        " VALUES('{}', '{}')".format(data[0], email))
    db.commit()
    return "signup"

@app.route('/pass_flight')
def pass_flight():
    source_filter = 'ankara'
    dest_filter = 'istanbul'

    cursor = db.cursor()
    cursor.execute("SELECT * FROM flight AS F NATURAL JOIN flight_arrival"
    " WHERE EXISTS(SELECT city_name, country FROM airport AS A WHERE F.dep_airport_name = A.airport_name AND city_name LIKE CONCAT('%', '{}', '%'))"
    " AND EXISTS(SELECT city_name, country FROM airport AS A WHERE F.arr_airport_name = A.airport_name AND city_name LIKE CONCAT('%', '{}', '%'))" 
    " ORDER BY F.flight_id".format(source_filter, dest_filter))
    
    pass_id = 7
    flight_id = 1
    ts = '2016-01-12 15:27:43'
    f = '%Y-%m-%d %H:%M:%S'
    deadline = datetime.datetime.strptime(ts, f)

    cursor.execute("INSERT INTO reservation(pass_id, flight_id, deadline)"
                   " VALUES('{}', '{}', '{}')".format(pass_id, flight_id, deadline))

    flight_id = 1
    pass_id = 7
    staff_id = 3

    cursor.execute("INSERT INTO ticket(flight_id, pass_id, staff_id)"
                    " VALUES('{}', '{}', '{}')".format(flight_id, pass_id, staff_id))
    db.commit()
    return "pass_flight"

@app.route('/pass_flight_history')
def pass_flight_history():
    cursor = db.cursor()
    create_pass_history_view()

    pass_id = 2
    cursor.execute("SELECT * FROM pass_history_view")
    data = cursor.fetchall()
    for row in data:
        for i in row:
            print row[i]

    drop_pass_history_view()
    flight_id = 2
    cursor.execute("DELETE FROM ticket WHERE pass_id = '{}' AND flight_id = '{}'".format(pass_id, flight_id))
    db.commit()

@app.route('/reservation')
def reservation():
    cursor = db.cursor()

    pass_id = 2
    cursor.execute("SELECT * FROM reservation WHERE pass_id = '{}'".format(pass_id))
    data = cursor.fetchall()
    for row in data:
        for i in row:
            print row[i]

    flight_id = 2
    cursor.execute("DELETE FROM reservation WHERE pass_id = '{}' AND flight_id = '{}'".format(pass_id, flight_id))
    db.commit()
    return "reservation"

@app.route('/store')
def store():
    cursor = db.cursor()

    airport_name = 'esenboga'

    cursor.execute("SELECT store_id, store_name, owner FROM store NATURAL JOIN airport "
                   "WHERE airport_name LIKE CONCAT('%', '{}', '%')".format(airport_name))
    data = cursor.fetchall()
    for row in data:
        for i in row:
            print row[i]
    return "store"

@app.route('/menu_option')
def menu_option():
    cursor = db.cursor()

    flight_id = 1

    cursor.execute("SELECT option_id, option_name "
                   "FROM menu_option WHERE flight_id = '{}'".format(flight_id))
    data = cursor.fetchall()
    for row in data:
        for i in row:
            print row[i]
    return "menu option"

@app.route('/pass_profile')
def pass_profile():
    cursor = db.cursor()

    person_id = 7

    cursor.execute("SELECT * FROM passenger WHERE pass_id = '{}'".format(person_id))
    data = cursor.fetchone()
    print data[0], data[1], data[2], data[3], data[4], data[5]
    return "passenger profile"

@app.route('/pilot_profile')
def pilot_profile():
    cursor = db.cursor()

    person_id = 8

    cursor.execute("SELECT * FROM pilot WHERE pilot_id = '{}'".format(person_id))
    data = cursor.fetchone()
    print data[0], data[1], data[2], data[3], data[4], data[5]
    return "pilot profile"

@app.route('/attendant_profile')
def attendant_profile():
    cursor = db.cursor()

    person_id = 9

    cursor.execute("SELECT * FROM flight_attendant WHERE att_id = '{}'".format(person_id))
    data = cursor.fetchone()
    print data[0], data[1], data[2], data[3], data[4], data[5]
    return "attendant profile"

@app.route('/ticket_st_profile')
def ticket_st_profile():
    cursor = db.cursor()

    person_id = 10

    cursor.execute("SELECT * FROM ticket_staff WHERE ticket_staff_id = '{}'".format(person_id))
    data = cursor.fetchone()
    print data[0], data[1], data[2], data[3], data[4], data[5]
    return "ticket_staff profile"

@app.route('/store_st_profile')
def store_st_profile():
    cursor = db.cursor()

    person_id = 11

    cursor.execute("SELECT * FROM store_staff WHERE store_staff_id = '{}'".format(person_id))
    data = cursor.fetchone()
    print data[0], data[1], data[2], data[3], data[4], data[5]
    return "store_staff profile"

def update_password(old, new, person_id):
    cursor = db.cursor()
    cursor.execute("SET person UPDATE password = '{}' WHERE password = '{}' "
                   "person_id = '{}'".format(new, old, person_id))
    db.commit()

def delete_phone(phone, person_id):
    cursor = db.cursor()
    cursor.execute("DELETE FR0M person_phone WHERE person_id = '{}' AND "
                   "phone = '{}'".format(person_id, phone))
    db.commit()

def add_phone(phone, person_id):
    cursor = db.cursor()
    cursor.execute("INSERT INTO person_phone VALUES(person_id, phone)")
    db.commit()

def delete_email(email, person_id):
    cursor = db.cursor()
    cursor.execute("DELETE FR0M person_email WHERE person_id = '{}' AND "
                   "email = '{}'".format(person_id, email))
    db.commit()

def add_email():
    cursor = db.cursor()
    cursor.execute("INSERT INTO person_email VALUES(person_id, email)")
    db.commit()

def delete_account(person_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM person WHERE person_id = '{}'".format(person_id))
    db.commit()

def create_pass_history_view():
    cursor = db.cursor()

    flight_pers_id = 3
    cursor.execute("CREATE VIEW pers_history_view AS"
                   " SELECT * FROM pers_history WHERE flight_pers_id = '{}'".format(flight_pers_id))

def drop_pass_history_view():
    cursor = db.cursor()
    cursor.execute("DROP VIEW pers_history_view")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3360, debug=True)
