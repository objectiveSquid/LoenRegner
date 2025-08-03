from config import DATA_DIRECTORY
from collections import OrderedDict
import datetime
import uuid
import json
from typing import Any


MONTH_READABLE = {
    1: "Januar",
    2: "Februar",
    3: "Marts",
    4: "April",
    5: "Maj",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "December",
}


def get_shifts(uuid: str) -> dict[str, Any]:
    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)
        return shifts.get(uuid)


def get_shifts_formatted(
    uuid: str,
) -> list[
    float
    | int
    | OrderedDict[str, float | int | dict[str, str | float | dict[str, Any]]],
]:
    shifts = get_shifts(uuid)
    # this type is wrong on purpose so i dont have to put #type:ignore on almost every line
    output = {}

    for shift in shifts.values():
        # output["programmer_date"][2] is the year
        # output["programmer_date"][1] is the month
        year, month = shift["programmer_date"][2], shift["programmer_date"][1]

        try:
            output[year]
        except KeyError:
            output[year] = {"months": OrderedDict(), "year": year, "wage": 0}

        try:
            output[year]["months"][month]
        except KeyError:
            output[year]["months"][month] = {
                "shifts": [],
                "month_number": MONTH_READABLE[month],
                "month": MONTH_READABLE[month],
                "wage": 0,
            }

        output[year]["months"][month]["shifts"].append(
            {
                "uuid": shift["uuid"],
                "programmer_time": shift["programmer_time"],
                "date": shift["date"],
                "start": shift["start"],
                "stop": shift["stop"],
                "wage": shift["wage"],
                "hourly": shift["hourly"],
            }
        )
        output[year]["months"][month]["wage"] += shift["wage"]
        output[year]["wage"] += shift["wage"]

        # sort individual shifts by programmer_time
        output[year]["months"][month]["shifts"].sort(
            key=lambda x: x["programmer_time"], reverse=True
        )

        # sort months
        output[year]["months"] = OrderedDict(
            sorted(output[year]["months"].items(), key=lambda x: x[0])
        )

    # sort years
    output = OrderedDict(sorted(output.items(), key=lambda x: x[0]))

    for year in output.values():
        year["months"] = list(year["months"].values())

    return list(output.values())


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

    programmer_time = int(
        datetime.datetime.fromisocalendar(
            programmer_date[2], programmer_date[1], programmer_date[0]
        ).strftime("%s")
    )

    shifts[user_uuid][shift_uuid] = {
        "uuid": shift_uuid,
        "date": date,
        "programmer_date": programmer_date,
        "programmer_time": programmer_time,
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
