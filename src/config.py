import os.path

STATIC_DIRECTORY = os.path.split(__file__)[0] + "/static"
TEMPLATES_DIRECTORY = os.path.split(__file__)[0] + "/html"
DATA_DIRECTORY = os.path.split(os.path.split(__file__)[0])[0] + "/data"

SESSION_TIMEOUT = 1000 * 60 * 60 * 24 * 7  # 7 days in milliseconds
