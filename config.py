import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'data', 'employees.db')
TABLE_NAME = 'employees'

REQUIREMENTS_HEADERS =  ['id', 'name', 'salary']

class ExitCode:
    SUCCESS = 0
    SYSTEM_ERROR = 1
    VALIDATE_ERROR = 2
    DATABASE_ERROR = 3


