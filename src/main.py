from flask import Flask
import os.path

STATIC_DIRECTORY = os.path.split(__file__)[0] + "/static"

app = Flask(__name__, static_folder=STATIC_DIRECTORY)


@app.route("/")
def index():
    return app.send_static_file("index.html")
