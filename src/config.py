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
