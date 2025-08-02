from flask import request, Flask, make_response, render_template
import os

from user import *
from shifts import *
from config import *

app = Flask(
    __name__, static_folder=STATIC_DIRECTORY, template_folder=TEMPLATES_DIRECTORY
)


def init():
    if os.path.isdir(DATA_DIRECTORY) is False:
        os.mkdir(DATA_DIRECTORY)

    if os.path.isfile(DATA_DIRECTORY + "/shifts.json") is False:
        with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
            shifts_fd.write("{}")

    if os.path.isfile(DATA_DIRECTORY + "/users.json") is False:
        with open(DATA_DIRECTORY + "/users.json", "w") as users_fd:
            users_fd.write("{}")


init()


@app.route("/", methods=["GET"])
def index():
    session = request.cookies.get("SessionID", "")

    if not isValidSessionID(session):
        return app.redirect("/login")  # user not logged in

    return app.redirect("/shifts")


@app.route("/getSessionID", methods=["POST"])
def getSessionID():
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return make_response("Missing parameters", 400)

    if (uuid := verifyCredentials(username, password)) is None:
        return make_response("Invalid username or password", 401)

    session = generateSessionID(uuid)

    return make_response(session, 200)


@app.route("/createAccount", methods=["POST"])
def createAccount():
    username = request.json.get("username")
    password = request.json.get("password")
    hourly = request.json.get("hourly")

    if username is None or password is None:
        return make_response("Missing parameters", 400)

    if userExists(username):
        return make_response("Username is taken", 409)

    uuid = createUser(username, password, hourly)

    return make_response(uuid, 200)


@app.route("/shifts", methods=["GET"])
def shifts():
    session = request.cookies.get("SessionID", "")

    if not isValidSessionID(session):
        return app.redirect("/login")

    user = getUserInfo(getUUID(session))
    shifts = getShifts(user["uuid"])

    return render_template("shifts.jinja2", user=user, shifts=shifts)


@app.route("/login", methods=["GET"])
def login():
    if isValidSessionID(request.cookies.get("SessionID", "")):
        return app.redirect("/shifts")

    return app.send_static_file("html/login.html")


@app.route("/signup", methods=["GET"])
def signup():
    if isValidSessionID(request.cookies.get("SessionID", "")):
        return app.redirect("/shifts")

    return app.send_static_file("html/signup.html")


@app.route("/add", methods=["POST"])
def calculate():
    session = request.cookies.get("SessionID", "")

    if not isValidSessionID(session):
        return app.redirect("/login")

    uuid = getUUID(session)
    if uuid is None:
        return make_response("Invalid session", 401)

    starttime = request.json.get("starttime")
    stoptime = request.json.get("stoptime")
    hourly = request.json.get("hourly")

    if starttime is None or stoptime is None or hourly is None:
        return make_response("Missing parameters", 400)

    if starttime.count(":") != 1 or stoptime.count(":") != 1:
        return make_response("Invalid time format", 400)

    if hourly.isnumeric() is False:
        return make_response("Hourly must be a number", 400)
    hourly = int(hourly)

    start_hour, start_minute = starttime.split(":")
    stop_hour, stop_minute = stoptime.split(":")

    try:
        start_hour = int(start_hour)
        start_minute = int(start_minute)
        stop_hour = int(stop_hour)
        stop_minute = int(stop_minute)
    except ValueError:
        return make_response("Invalid time format", 400)

    start_time_minutes = start_hour * 60 + start_minute
    stop_time_minutes = stop_hour * 60 + stop_minute

    if stop_time_minutes < start_time_minutes:
        return make_response("Stop time must be after start time", 400)

    hours_worked = (stop_time_minutes - start_time_minutes) / 60
    total_pay = hours_worked * hourly

    minutes_worked = stop_time_minutes - start_time_minutes
    time_worked_pretty = f"{int(hours_worked)}:{minutes_worked % 60}"

    addShift(uuid, starttime, stoptime, time_worked_pretty, total_pay, hourly)

    return make_response("Shift added", 200)
