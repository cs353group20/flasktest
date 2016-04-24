from flask import Flask, render_template, request, Response, session, g
import flask
import json
import requests
import functools
import mysql.connector
from mysql.connector import errorcode
from subprocess import call
import data

app = Flask(__name__)
app.config.update(dict(
    DATABASE="airline_company",
    DEBUG=True,
    SECRET_KEY='eskihafiz',
    USER="root",
    PASS="kaan"
))

def connect_db():
    db = mysql.connector.connect(user=app.config['USER'], passwd=app.config['PASS'])
    try:
        db.database = app.config['DATABASE']
    except mysql.connector.Error as err:
        return None
    return data.database(db)

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        #session.pop('isloggedin', None)
        if 'isloggedin' in session:
            return method(*args, **kwargs)
        else:
            return flask.redirect('/login')
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    if 'isloggedin' in session:
        return flask.redirect('/')

    if request.method == 'POST':
        if 'id' in request.form and 'password' in request.form:
            userid = request.form['id']
            password = request.form['password']
            if db.check_login(userid, password):
                session['id'] = userid
                session['isloggedin'] = True
                session['user_type'] = db.get_user_type(userid)
                return flask.redirect('/')
            else:
                return flask.redirect('/login')

    return render_template('login.html')

@app.route('/')
@login_required
def init_screen():
    return session['user_type']

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3131, debug=True)
