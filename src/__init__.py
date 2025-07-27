import os

STATIC_DIRECTORY = os.path.split(__file__)[0] + "/static"

DATA_DIRECTORY = os.path.split(os.path.split(__file__)[0])[0] + "/data"


def init():
    if os.path.isdir(DATA_DIRECTORY) is False:
        os.mkdir(DATA_DIRECTORY)

    if os.path.isfile(DATA_DIRECTORY + "/shifts.json") is False:
        with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
            shifts_fd.write("{}")
