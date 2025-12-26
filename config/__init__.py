from .loader import load_config

config = load_config()

EXIT_CODE = config.ExitCode

DB_PATH = config.DB_PATH
TABLE_NAME = config.TABLE_NAME
ALLOWED_TABLES_NAME = config.ALLOWED_TABLES_NAME

REQUIREMENTS_HEADERS = config.REQUIREMENTS_HEADERS

LOG_DIR = config.LOG_DIR
LOG_FILE = config.LOG_FILE
LOG_LEVEL = config.LOG_LEVEL