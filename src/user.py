from . import DATA_DIRECTORY
import json


def getUser(session: str) -> dict:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)
        return users.get(session)


def isValidSessionID(sessionID: str) -> bool:
    return getUser(sessionID) is not None
