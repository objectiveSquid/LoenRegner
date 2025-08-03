from config import DATA_DIRECTORY
import uuid
import json


def add_shift(
    user_uuid: str,
    date: str,
    starttime: str,
    stoptime: str,
    duration: str,
    wage: float,
    hourly: float,
) -> None:
    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)

    shift_uuid = uuid.uuid4().hex
    programmer_date = []

    # caller has already checked that date is in correct format, which is `%d/%m/%Y`
    for element in date.split("/"):
        programmer_date.append(int(element))

    shifts[user_uuid][shift_uuid] = {
        "uuid": shift_uuid,
        "date": date,
        "programmer_date": programmer_date,
        "start": starttime,
        "stop": stoptime,
        "duration": duration,
        "wage": wage,
        "hourly": hourly,
    }

    with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
        json.dump(shifts, shifts_fd, indent=4)


def delete_shift(user_uuid: str, shift_uuid: str) -> None:
    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)

    try:
        del shifts[user_uuid][shift_uuid]
    except KeyError:
        return  # user uuid or shift uuid doesnt exist

    with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
        json.dump(shifts, shifts_fd, indent=4)
