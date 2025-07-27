from flask import request, Flask, make_response, render_template
import os.path
import json

from .user import *
from . import DATA_DIRECTORY, STATIC_DIRECTORY

app = Flask(__name__, static_folder=STATIC_DIRECTORY)


@app.route("/", methods=["GET"])
def index():
    session = request.cookies.get("SessionID", "")

    if not isValidSessionID(session):
        return app.send_static_file("html/index.html")  # user not logged in

    return app.redirect("/shifts")


@app.route("/shifts", methods=["GET"])
def shifts():
    session = request.cookies.get("SessionID", "")

    if not isValidSessionID(session):
        return app.redirect("/")

    return render_template("html/shifts.html", session=session)


@app.route("/add", methods=["POST"])
def calculate():
    starttime = request.form.get("starttime")
    stoptime = request.form.get("stoptime")
    hourly = request.form.get("hourly")

    print(starttime, stoptime, hourly)

    if starttime is None or stoptime is None or hourly is None:
        return make_response("Missing parameters", 400)

    if starttime.count(":") != 1 or stoptime.count(":") != 1:
        return make_response("Invalid time format", 400)

    if hourly.isnumeric() is False:
        return make_response("Hourly must be a number", 400)

    start_hour, start_minute = starttime.split(":")
    stop_hour, stop_minute = stoptime.split(":")

    try:
        start_time = int(start_hour) * 60 + int(start_minute)
        stop_time = int(stop_hour) * 60 + int(stop_minute)
    except ValueError:
        return make_response("Invalid time format", 400)

    if stop_time < start_time:
        return make_response("Stop time must be after start time", 400)

    hours_worked = (stop_time - start_time) / 60
    total_pay = hours_worked * int(hourly)

    return make_response(f"Total pay: {total_pay}", 200)
