from config import DATA_DIRECTORY, SESSION_TIMEOUT
from typing import Any
import time
import hashlib
import uuid
import json


def get_user_info(uuid: Any) -> dict[str, Any]:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)
        return users.get(uuid)


def get_shifts(uuid: str) -> dict[str, Any]:
    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)
        return shifts.get(uuid)


def get_UUID(sessionID: str) -> str | None:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    for user in users.values():
        for session, expiration in user["sessions"].items():
            if session == sessionID and expiration > int(round(time.time() * 1000)):
                return user["uuid"]

    return None


def is_valid_sessionID(sessionID: str) -> bool:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    for user in users.values():
        for session, expiration in user["sessions"].items():
            if session == sessionID and expiration > int(round(time.time() * 1000)):
                return True

    return False


def generate_password_hash(password: str, salt: str) -> str:
    return hashlib.sha256(password.encode() + salt.encode()).hexdigest()


def generate_sessionID(target_uuid: str) -> str:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    user = users.get(target_uuid)

    session_id = uuid.uuid4().hex
    user["sessions"][session_id] = int(round(time.time() * 1000 + SESSION_TIMEOUT))

    with open(DATA_DIRECTORY + "/users.json", "w") as users_fd:
        json.dump(users, users_fd, indent=4)

    return session_id


def verify_credentials(username: str, password: str) -> str | None:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    for uuid, user in users.items():
        if user["username"] == username and user["password"] == generate_password_hash(
            password, user["salt"]
        ):
            return uuid

    return None


def user_exists(username: str) -> bool:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    for user in users.values():
        if user["username"] == username:
            return True

    return False


def create_user(username: str, password: str, hourly: int) -> str:
    with open(DATA_DIRECTORY + "/users.json", "r") as users_fd:
        users = json.load(users_fd)

    new_uuid = uuid.uuid4().hex
    while new_uuid in users.keys():
        new_uuid = uuid.uuid4().hex  # will likely never happen

    salt = uuid.uuid4().hex

    users[new_uuid] = {
        "uuid": new_uuid,  # duplicate field for convienience
        "hourly": hourly,
        "username": username,
        "password": generate_password_hash(password, salt),
        "salt": salt,
        "sessions": {},  # a dict like: `{session_id_string: expiration_epoch_time, ...}`
    }

    with open(DATA_DIRECTORY + "/users.json", "w") as users_fd:
        json.dump(users, users_fd)

    with open(DATA_DIRECTORY + "/shifts.json", "r") as shifts_fd:
        shifts = json.load(shifts_fd)

    shifts[new_uuid] = []

    with open(DATA_DIRECTORY + "/shifts.json", "w") as shifts_fd:
        json.dump(shifts, shifts_fd)

    return new_uuid
