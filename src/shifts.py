from config import DATA_DIRECTORY
import datetime
import json


def addShift(
    uuid: str,
    starttime: str,
    stoptime: str,
    duration: str,
    wage: float,
    hourly: float,
) -> None:
    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)

    shifts[uuid].append(
        {
            "date": datetime.datetime.now().strftime("%d/%m/%Y"),
            "start": starttime,
            "stop": stoptime,
            "duration": duration,
            "wage": wage,
            "hourly": hourly,
        }
    )

    with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
        json.dump(shifts, shifts_fd)
