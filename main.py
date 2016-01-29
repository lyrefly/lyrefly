import config.config as project_config
import calendar, time
import Image
import os

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
    for f in os.listdir(join(app.config['UPLOAD_FOLDER'], "650/")):
        if isfile(join(app.config['UPLOAD_FOLDER'], "650/", f)):
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
        filename = str(calendar.timegm(time.gmtime())) + "_" + data.filename
        path = join(app.config['UPLOAD_FOLDER'], filename)
        data.save(path)
        make_thumb(filename, 650)
        flash("Uploaded: " + data.filename)
    else:
        flash("No file uploaded! ")
    return render_template("submit.html")

def make_thumb(name, size):
    dimensions = size, size
    thumb_dir = join(app.config['UPLOAD_FOLDER'], str(size))
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)

    try:
        img = Image.open(join(app.config['UPLOAD_FOLDER'], name))
        img.thumbnail(dimensions)
        img.save(join(thumb_dir, name))
    except IOError:
        print("Thumbnail generation failed!")

if __name__ == "__main__":
    app.run()
