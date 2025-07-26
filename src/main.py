from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    with open("static/index.html", "r") as fd:
        return fd.read()
