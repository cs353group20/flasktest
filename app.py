from flask import Flask, render_template, request, Response, session
import flask
import json
import requests
import functools
import pymongo
import MySQLdb
from subprocess import call
from redis import Redis

app = Flask(__name__)
app.secret_key = "eskihafiz"
db = MySQLdb.connect('localhost', 'root', 'omer', 'DENEME')

def login_required(method):
    '''
    This is a decorator to protect the pages and the operations that need user to be logged in to see/do.
    '''
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'isloggedin' in session:
            return method(*args, **kwargs)
        else:
            return flask.redirect('/login')
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'isloggedin' in session:
        print("AHANDA")
        return flask.redirect('/')
    else:
        print("DENME")
    if request.method == 'POST':
        if 'id' in request.form and 'password' in request.form:
            username = request.form['id']
            password = request.form['password']
            cursor = db.cursor()
            cursor.execute("SELECT * from user WHERE username='{}' and pass='{}'".format(username, password))
            data = cursor.fetchone()
            if data == None:
                return flask.redirect('/login')
            session['id'] = request.form['id']
            session['isloggedin'] = True
            return flask.redirect('/')
        return flask.redirect('/login')
    else:
        return render_template('login.html')


@app.route('/')
@login_required
def dashboard_html():
    if 'id' in session:
        return "HOSGELDIN {}".format(session['id'])
    else:
        return "NOPE"

"""
@app.route('/test_metric', methods=['POST'])
@login_required
def test_metric():
    r = requests.get("http://analytics.scorebeyond.com:8000/v1/new_metric", data = request.data)
    res = Response(response = json.dumps({"response":json.loads(r.text), "status":r.status_code}), status = 200, mimetype = "application/json")
    return res

@app.route('/add_metric', methods=['POST'])
@login_required
def add_metric():
    r = requests.post("http://analytics.scorebeyond.com:8000/v1/new_metric", data = request.data)
    res = Response(response = json.dumps({"response":json.loads(r.text), "status":r.status_code}), status = 200, mimetype = "application/json")
    return res

def erase_metric_data(metric):
	db = pymongo.mongo_client.MongoClient(host='localhost')['analytics']
	db.calculable_result.remove({"name":metric})
	folder_path = "/opt/graphite/storage/whisper/" + metric
	call(["rm", "-rf", folder_path]) # delete graphite data!!!
	r = Redis()
	r.hdel("calculable_times", *[metric]) # delete last_calculable_time from redis.

def erase_metric_from_db(metric):
	db = pymongo.mongo_client.MongoClient(host='localhost')['analytics']
	db.calculable_definition.remove({"name":metric})

@app.route('/reset_metric', methods=['POST'])
@login_required
def reset_metric():
	data = json.loads(request.data)
	if 'name' in data:
		erase_metric_data(data['name'])
	res = Response(response = json.dumps({}), status = 200, mimetype = "application/json")
 	return res

@app.route('/delete_metric', methods=['POST'])
@login_required
def delete_metric():
	data = json.loads(request.data)
	if 'name' in data:
		erase_metric_data(data['name'])
		erase_metric_from_db(data['name'])
	res = Response(response = json.dumps({}), status = 200, mimetype = "application/json")
 	return res
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
