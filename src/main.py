from flask import request, Flask, make_response
import os.path

STATIC_DIRECTORY = os.path.split(__file__)[0] + "/static"

app = Flask(__name__, static_folder=STATIC_DIRECTORY)


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    starttime = request.form.get("starttime")
    stoptime = request.form.get("starttime")
    hourly = request.form.get("hourly")

    if starttime is None or stoptime is None:
        return make_response("Missing starttime or stoptime", 400)

    return "TODO"
