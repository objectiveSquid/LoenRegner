import os.path

# paths
STATIC_DIRECTORY = os.path.split(__file__)[0] + "/static"
TEMPLATES_DIRECTORY = os.path.split(__file__)[0] + "/html"
DATA_DIRECTORY = os.path.split(os.path.split(__file__)[0])[0] + "/data"

# tax stuff, names are somewhat in danish
AM_BIDRAG_MULTIPLIER = 0.92
FRIKORT_LIMIT = 51_600
BUNDSKAT = 0.1201  # 12.01% på bundskat
TOPSKAT_CUTOFF = 611_800  # DKK
TOPSKAT = 0.15  # 15% på toplønnere

# defaults
DEFAULT_HOURLY = 100
DEFAULT_TAX_START = FRIKORT_LIMIT

# other
SESSION_TIMEOUT = 1000 * 60 * 60 * 24 * 7  # 7 days in milliseconds
MINIMUM_PASSWORD_CHARACTERS = 4

# admin, shouldnt be imported
_ADMIN_CREDENTIAL: str = ""
_ADMIN_SESSION_ID: str = ""


def load_admin_credentials():
    global _ADMIN_CREDENTIAL, _ADMIN_SESSION_ID

    try:
        with open(f"{DATA_DIRECTORY}/.env", "r") as env_fd:
            lines = [
                line.strip() for line in env_fd.read().splitlines() if line.strip()
            ]
    except Exception:
        print("COULD NOT LOAD .env FILE, PANICKING.")
        exit(1)

    if len(lines) != 2:
        print("INVALID .env FILE CONTENT, PANICKING.")
        exit(1)

    _ADMIN_CREDENTIAL = lines[0]
    _ADMIN_SESSION_ID = lines[0]


def get_admin_username() -> str:
    global _ADMIN_CREDENTIAL

    return _ADMIN_CREDENTIAL


def get_admin_password() -> str:
    global _ADMIN_CREDENTIAL

    return _ADMIN_CREDENTIAL


def get_admin_session_id() -> str:
    global _ADMIN_SESSION_ID

    return _ADMIN_SESSION_ID
