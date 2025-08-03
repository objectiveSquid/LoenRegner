from collections import OrderedDict
import datetime
import uuid
import json
from typing import Any

from user import get_user_info
from config import *


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
    user_info = get_user_info(uuid)
    output = {}

    for shift in shifts.values():
        # output["programmer_date"][2] is the year
        # output["programmer_date"][1] is the month
        year, month = shift["programmer_date"][2], shift["programmer_date"][1]

        try:
            output[year]
        except KeyError:
            output[year] = {
                "months": OrderedDict(),
                "year": year,
                "wage": 0,
                "hours": 0,
            }

        try:
            output[year]["months"][month]
        except KeyError:
            output[year]["months"][month] = {
                "shifts": [],
                "month_number": MONTH_READABLE[month],
                "month": MONTH_READABLE[month],
                "wage": 0,
                "hours": 0,
            }

        output[year]["months"][month]["shifts"].append(
            {
                "uuid": shift["uuid"],
                "programmer_time": shift["programmer_time"],
                "date": shift["date"],
                "start": shift["start"],
                "stop": shift["stop"],
                "wage": shift["wage"],
                "wage_after_am": shift["wage"] * AM_BIDRAG_MULTIPLIER,
                "hourly": shift["hourly"],
            }
        )
        output[year]["months"][month]["wage"] += shift["wage"]
        output[year]["months"][month]["hours"] += shift["wage"] / shift["hourly"]

        output[year]["wage"] += shift["wage"]
        output[year]["hours"] += shift["wage"] / shift["hourly"]

        # sort individual shifts by programmer_time
        output[year]["months"][month]["shifts"].sort(
            key=lambda x: x["programmer_time"], reverse=True
        )

        # sort months
        output[year]["months"] = OrderedDict(
            sorted(output[year]["months"].items(), key=lambda x: x[0], reverse=True)
        )

    # sort years
    output = OrderedDict(sorted(output.items(), key=lambda x: x[0], reverse=True))

    for year in output.values():
        year["months"] = list(year["months"].values())

    # calculate "am-bidrag" and taxes
    for year in output.values():
        year["taxed_wage"] = year["wage"] * AM_BIDRAG_MULTIPLIER

        if year["taxed_wage"] > user_info["tax_start"]:
            if year["taxed_wage"] > TOPSKAT_CUTOFF:
                tax = TOPSKAT
            else:
                tax = BUNDSKAT

            year["taxed_wage"] -= (year["taxed_wage"] - user_info["tax_start"]) * tax

        for month in year["months"]:
            month["wage_after_am"] = month["wage"] * AM_BIDRAG_MULTIPLIER

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
