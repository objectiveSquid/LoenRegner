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
_ADMIN_USERNAME: str = ""
_ADMIN_PASSWORD: str = ""


def load_admin_credentials():
    global _ADMIN_USERNAME, _ADMIN_PASSWORD

    print(os.getcwd())
    try:
        with open(".env", "r") as env_fd:
            lines = [
                line.strip() for line in env_fd.read().splitlines() if line.strip()
            ]
    except Exception:
        print("COULD NOT LOAD .env FILE, PANICKING.")
        exit(1)

    if len(lines) != 2:
        print("INVALID .env FILE CONTENT, PANICKING.")
        exit(1)

    _ADMIN_USERNAME = lines[0].casefold()
    _ADMIN_PASSWORD = lines[1]


def get_admin_username():
    return _ADMIN_USERNAME


def get_admin_password():
    return _ADMIN_PASSWORD
