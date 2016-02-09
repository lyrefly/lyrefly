import config.config as project_config

# Import the Flask Framework
from flask import Flask
import calendar, time
from PIL import Image
import os
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from os.path import isfile, join
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app.config.from_object(project_config)

@app.route("/")
def home():
    images = []
    """for f in os.listdir(join(app.config['UPLOAD_FOLDER'], "650/")):
        if isfile(join(app.config['UPLOAD_FOLDER'], "650/", f)):
            images.append(f)"""
    image_data = {}
    image_data['even'] = images[::2]
    image_data['odd'] = images[1::2]
    return render_template("index.html", images=image_data)


@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/login/", methods=['POST'])
def login_post():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/register/", methods=['POST'])
def register_post():
    return render_template("register.html")

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

def make_thumb(name, size):
    dimensions = size, size


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
