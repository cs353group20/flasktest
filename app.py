from flask import Flask, render_template, request, Response, session
import flask
import json
import requests
import functools
import MySQLdb
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

@app.route('/')
@login_required
def init_screen():
    pass

@app.route('/signup', methods=['GET', 'POST'])
@signup_required
def signup():
    session.pop('signup', None)
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3360, debug=True)
