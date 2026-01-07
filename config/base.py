import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')

POSTGRES = {
    'user': os.getenv('POSTGRES_USER', "user"),
    'password': os.getenv('POSTGRES_PASSWORD', 'password123'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'db_name')
}


def get_database_url():
    return (
        f"postgresql://"
        f"{POSTGRES['user']}:{POSTGRES['password']}@"
        f"{POSTGRES['host']}:{POSTGRES['port']}/"
        f"{POSTGRES['database']}"
    )


class ExitCode:
    SUCCESS = 0
    SYSTEM_ERROR = 1
    VALIDATE_ERROR = 2
    DATABASE_ERROR = 3


BASE_DIR = Path(__file__).resolve().parent.parent
APP_NAME = 'csv_validator'

REQUIREMENTS_HEADERS = ['id', 'name', 'salary']

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
LOG_LEVEL = 'INFO'
