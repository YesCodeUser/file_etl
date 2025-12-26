from pathlib import Path

class ExitCode:
    SUCCESS = 0
    SYSTEM_ERROR = 1
    VALIDATE_ERROR = 2
    DATABASE_ERROR = 3


BASE_DIR = Path(__file__).resolve().parent.parent
APP_NAME = 'csv_validator'
ENV = 'base'

DB_PATH = BASE_DIR / 'data' / 'employees.db'
TABLE_NAME = 'employees'
ALLOWED_TABLES_NAME = [
    'employees', 'employee',
    'users', 'user'
]

REQUIREMENTS_HEADERS = ['id', 'name', 'salary']

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
LOG_LEVEL = 'INFO'