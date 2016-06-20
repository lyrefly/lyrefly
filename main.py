# Import the Flask Framework
from flask import Flask
import calendar, time
from PIL import Image
import os
import datetime

import logging
# logging.info("hello")

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route("/")
def home():
    image_data = {}
    return render_template("index.html", images=image_data, username="")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/login/", methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    return ""

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/register/", methods=['POST'])
def register_post():
    return ""

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
    return ""

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
