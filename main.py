
# Import the Flask Framework
from flask import Flask
import calendar, time
from PIL import Image
from Crypto.Hash import SHA256
import MySQLdb
import os
import datetime
from base64 import b64encode
from py2casefold import casefold


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def home():
    images = []
    """for f in os.listdir(join(app.config['UPLOAD_FOLDER'], "650/")):
        if isfile(join(app.config['UPLOAD_FOLDER'], "650/", f)):
            images.append(f)"""
    image_data = {}
    image_data['even'] = images[::2]
    image_data['odd'] = images[1::2]
    loginID = check_login()
    return render_template("index.html", images=image_data, username=get_casename(loginID))


@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/login/", methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    login_request = loginUP(username, password)
    if type(login_request) is str:
        flash(login_request)
        return render_template("login.html")
    return login_request

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/register/", methods=['POST'])
def register_post():
    casename = request.form['username']
    username = casefold(casename)
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    #Validate Input Here
    if password != password2: #Check password match
        flash("Your passwords don't match!")
        return render_template("register.html")

    #Check if username is available
    db = connect_to_database()
    cur = db.cursor()
    exists = cur.execute('SELECT 1 FROM Users WHERE Username = %s', (username,))
    db.close()
    if exists >= 1:
        flash("Sorry, that username is taken.")
        return render_template("register.html")

    random_bytes = os.urandom(32)
    salt = b64encode(random_bytes).decode('utf-8')
    userHash = SHA256.new(password + salt).hexdigest()

    db = connect_to_database()
    cur = db.cursor()
    cur.execute('INSERT INTO Users (Username, Casename, Email, Salt, Hash) VALUES (%s, %s, %s, %s, %s)',
        (username, casename, email, salt, userHash))
    db.commit()
    db.close()
    login_request = loginUP(username, password)
    return login_request

@app.route("/search/", methods=['GET'])
def search():
    return render_template("search.html")

@app.route("/submit/")
def submit():
    return render_template("submit.html")

@app.route("/submit/", methods=['POST'])
def submit_post():
    data = request.files['file']
    if data:
        filename = str(calendar.timegm(time.gmtime())) + "_" + data.filename
        flash("Uploaded: " + data.filename)
    else:
        flash("No file uploaded! ")
    return render_template("submit.html")

@app.route("/logout/")
def logout():
    db = connect_to_database()
    cur = db.cursor()
    session_code = request.cookies.get('session_code')
    cur.execute('DELETE FROM Sessions WHERE Code = %s', (session_code,))
    resp = make_response(render_template("index.html", images={}))
    resp.set_cookie('session_code', expires=0)
    db.commit()
    db.close()
    return resp

def make_thumb(name, size):
    dimensions = size, size

def loginUP(username, password):
    #Check if the username and password are correct
    username = casefold(username)
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Users WHERE Username = %s', (username,))
    user = cur.fetchone()
    if user is None:
        db.close()
        return "We couldn't find a user registered with that name."
    UserID = user[0]
    salt = user[4]
    dbHash = user[5]
    userHash = SHA256.new(password + salt).hexdigest()
    if userHash != dbHash:
        db.close()
        return "Your password is incorrect."
    #So far so good, time to set a cookie
    session_code = b64encode(os.urandom(32)).decode('utf-8') #Generate the session code
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=app.config["COOKIE_DURATION"]) #Set the expiration date
    #Add the saved session to the database
    cur.execute('INSERT INTO Sessions (Code, UserID, Expires) VALUES (%s, %s, DATE(NOW()) + interval %s day)', (session_code, UserID, app.config["COOKIE_DURATION"]))
    db.commit()
    resp = make_response(render_template("index.html", images={}, username=user[2]))
    resp.set_cookie('session_code', session_code, expires=expire_date)
    db.close()
    return resp

def check_login():
    session_code = request.cookies.get('session_code')
    if session_code is None:
        return None
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Sessions WHERE Code = %s AND Expires > DATE(NOW())', (session_code,))
    found_session = cur.fetchone()
    if found_session is None:
        db.close()
        return None
    db.close()
    return found_session[1]

def get_casename(id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT Casename FROM Users WHERE UserID = %s', (id,))
    user = cur.fetchone()
    db.close()
    if user is None:
        return None
    return user[0]

def connect_to_database():
    _INSTANCE_NAME = app.config["INSTANCE_NAME"]
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME,
            db=app.config["DB_DATABASE"], user='root', charset='utf8')
    else:
        db = MySQLdb.connect(host=app.config["DB_HOST"],port=app.config["DB_PORT"],
            db=app.config["DB_DATABASE"], user=app.config["DB_USER"], passwd=app.config["DB_PASSWORD"],
            charset='utf8')
    return db

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
