import config as project_config

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__, static_url_path='/static')
app.config.from_object(project_config)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit")
def submit():
    return render_template("submit.html")

if __name__ == "__main__":
    app.run()
