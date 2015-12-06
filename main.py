import config.config as project_config
import calendar, time

from os import listdir
from os.path import isfile, join
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__, static_url_path='/static')
app.config.from_object(project_config)

@app.before_request
def before_request():
    return

@app.teardown_request
def teardown_request(exception):
    return 

@app.route("/")
def home():
    images = []
    for f in listdir("static/uploads/"):
        if isfile(join("static/uploads/", f)):
            images.append(f)
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
        data.save("static/uploads/" + str(calendar.timegm(time.gmtime())) + "_" + data.filename)
        flash("Uploaded: " + data.filename)
    else:
        flash("No file uploaded! ")
    return render_template("submit.html")

if __name__ == "__main__":
    app.run()
