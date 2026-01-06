import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_BACKEND = os.getenv('DB_BACKEND')

POSTGRES = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': int(os.getenv('POSTGRES_PORT')),
    'database': os.getenv('POSTGRES_DATABASE')
}

def get_database_url():
    if DB_BACKEND == 'postgres':
        return (
            f"postgresql://"
            f"{POSTGRES['user']}:{POSTGRES['password']}@"
            f"{POSTGRES['host']}:{POSTGRES['port']}/"
            f"{POSTGRES['database']}"
        )
    raise RuntimeError("Unsupported DB backend")


class ExitCode:
    SUCCESS = 0
    SYSTEM_ERROR = 1
    VALIDATE_ERROR = 2
    DATABASE_ERROR = 3

BASE_DIR = Path(__file__).resolve().parent.parent
APP_NAME = 'csv_validator'
ENV = 'base'

REQUIREMENTS_HEADERS = ['id', 'name', 'salary']

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = BASE_DIR / 'logs' / 'app.log'
LOG_LEVEL = 'INFO'