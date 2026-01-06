from .loader import load_config

config = load_config()

DB_BACKEND = config.DB_BACKEND
POSTGRES = config.POSTGRES

EXIT_CODE = config.ExitCode

REQUIREMENTS_HEADERS = config.REQUIREMENTS_HEADERS

LOG_DIR = config.LOG_DIR
LOG_FILE = config.LOG_FILE
LOG_LEVEL = config.LOG_LEVEL

get_database_url = config.get_database_url