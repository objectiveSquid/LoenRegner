from flask import request, Flask, make_response, render_template, jsonify, redirect
import os
import datetime

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
def index_page():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")  # user not logged in

    return redirect("/shifts")


@app.route("/shifts", methods=["GET"])
def shifts_page():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")

    user = get_user_info(get_UUID(session))
    shifts = get_shifts_formatted(user["uuid"])

    return render_template(
        "shifts.jinja2",
        user=user,
        shifts=shifts,
        default_date=datetime.datetime.now().strftime("%d/%m/%Y"),
    )


@app.route("/login", methods=["GET"])
def login_page():
    if is_valid_sessionID(request.cookies.get("SessionID", "")):
        return redirect("/shifts")

    return app.send_static_file("html/login.html")


@app.route("/signup", methods=["GET"])
def signup_page():
    if is_valid_sessionID(request.cookies.get("SessionID", "")):
        return redirect("/shifts")

    return app.send_static_file("html/signup.html")


@app.route("/add", methods=["POST"])
def add_shift_endpoint():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")

    uuid = get_UUID(session)
    if uuid is None:
        return make_response(jsonify({"status": "Invalid session"}), 401)

    date = request.json.get("date")
    starttime = request.json.get("starttime")
    stoptime = request.json.get("stoptime")
    hourly = request.json.get("hourly")

    if date is None:
        date = datetime.datetime.now().strftime("%d/%m/%Y")

    if date.count("/") != 2:
        return make_response(jsonify({"status": "Invalid date format"}), 400)
    elif not all(element.isnumeric() for element in date.split("/")):
        return make_response(jsonify({"status": "Invalid date format"}), 400)

    if starttime is None or stoptime is None or hourly is None:
        return make_response(jsonify({"status": "Missing parameters"}), 400)

    if starttime.count(":") != 1 or stoptime.count(":") != 1:
        return make_response(jsonify({"status": "Invalid time format"}), 400)

    if hourly.isnumeric() is False:
        return make_response(jsonify({"status": "Hourly must be a number"}), 400)
    hourly = int(hourly)

    start_hour, start_minute = starttime.split(":")
    stop_hour, stop_minute = stoptime.split(":")

    try:
        start_hour = int(start_hour)
        start_minute = int(start_minute)
        stop_hour = int(stop_hour)
        stop_minute = int(stop_minute)
    except ValueError:
        return make_response(jsonify({"status": "Invalid time format"}), 400)

    start_time_minutes = start_hour * 60 + start_minute
    stop_time_minutes = stop_hour * 60 + stop_minute

    if stop_time_minutes < start_time_minutes:
        return make_response(
            jsonify({"status": "Stop time must be after start time"}), 400
        )

    hours_worked = (stop_time_minutes - start_time_minutes) / 60
    total_pay = hours_worked * hourly

    minutes_worked = stop_time_minutes - start_time_minutes
    time_worked_pretty = f"{int(hours_worked)}:{minutes_worked % 60}"

    add_shift(uuid, date, starttime, stoptime, time_worked_pretty, total_pay, hourly)

    return make_response(jsonify({"status": "Shift added"}), 200)


@app.route("/delete", methods=["POST"])
def delete():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")

    uuid = get_UUID(session)
    if uuid is None:
        return make_response(jsonify({"status": "Invalid session"}), 401)

    shift_uuid = request.json.get("uuid")

    if shift_uuid is None:
        return make_response(jsonify({"status": "Missing parameters"}), 400)

    delete_shift(uuid, shift_uuid)

    return make_response(jsonify({"status": "Shift deleted"}), 200)


@app.route("/getSessionID", methods=["POST"])
def get_sessionID_endpoint():
    username = request.json.get("username")
    password = request.json.get("password")

    if username is None or password is None:
        return make_response(jsonify({"status": "Missing parameters"}), 400)

    if (uuid := verify_credentials(username, password)) is None:
        return make_response(jsonify({"status": "Invalid username or password"}), 401)

    session = generate_sessionID(uuid)

    return make_response(session, 200)


@app.route("/createAccount", methods=["POST"])
def create_account_endpoint():
    username = request.json.get("username")
    password = request.json.get("password")
    hourly = request.json.get("hourly")

    if username is None or password is None:
        return make_response(jsonify({"status": "Missing parameters"}), 400)

    if user_exists(username):
        return make_response(jsonify({"status": "Username is taken"}), 409)

    uuid = create_user(username, password, hourly)

    return make_response(uuid, 200)


@app.route("/logout", methods=["POST"])
def logout_endpoint():
    session = request.cookies.get("SessionID", "")

    invalidate_sessionID(session)

    response = make_response(jsonify({"status": "Logged out"}), 200)
    response.delete_cookie(
        "SessionID"
    )  # this is also done in the javascript, but just to make sure
    return response


@app.route("/deleteAccount", methods=["POST"])
def delete_account_endpoint():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")

    uuid = get_UUID(session)
    if uuid is None:
        return make_response(jsonify({"status": "Invalid session"}), 401)

    delete_user(uuid)

    return make_response(jsonify({"status": "Account deleted"}), 200)


@app.route("/changePassword", methods=["POST"])
def change_password_endpoint():
    session = request.cookies.get("SessionID", "")

    if not is_valid_sessionID(session):
        return redirect("/login")

    uuid = get_UUID(session)
    if uuid is None:
        return make_response(jsonify({"status": "Invalid session"}), 401)

    user_info = get_user_info(uuid)

    old_password = request.json.get("oldPassword")
    new_password = request.json.get("newPassword")

    if old_password is None or new_password is None:
        return make_response(jsonify({"status": "Missing parameters"}), 400)

    if verify_credentials(user_info["username"], old_password) is None:
        return make_response(jsonify({"status": "Invalid old password"}), 401)

    change_password(uuid, new_password)

    return make_response(jsonify({"status": "Password changed"}), 200)
