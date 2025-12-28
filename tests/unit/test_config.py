from pathlib import Path
import config

from config import base
from config import prod
from config import dev

class ConfigValidationHelper:

    @staticmethod
    def db_path_is_valid():
        assert isinstance(config.DB_PATH, Path)
        assert config.DB_PATH is not None
        assert config.DB_PATH.suffix in ['.db', '.sqlite', '.sqlite3']

    @staticmethod
    def table_name_is_valid():
        assert isinstance(config.TABLE_NAME, str)
        assert config.TABLE_NAME.strip() != ''
        assert config.TABLE_NAME in config.ALLOWED_TABLES_NAME

    @staticmethod
    def allowed_tables_name_is_valid():
        assert isinstance(config.ALLOWED_TABLES_NAME, list)
        for value in config.ALLOWED_TABLES_NAME:
            assert isinstance(value, str)

        assert config.ALLOWED_TABLES_NAME != []

    @staticmethod
    def requirements_headers_is_valid():
        assert isinstance(config.REQUIREMENTS_HEADERS, list)
        for value in config.REQUIREMENTS_HEADERS:
            assert isinstance(value, str)
        assert config.REQUIREMENTS_HEADERS != []

    @staticmethod
    def log_level_is_valid():
        assert isinstance(config.LOG_LEVEL, str)
        assert config.LOG_LEVEL.strip() != ''

    @staticmethod
    def log_dir_is_valid():
        assert isinstance(config.LOG_DIR, Path)
        assert config.LOG_DIR is not None
        assert config.LOG_FILE.exists()
        assert config.LOG_DIR.is_dir()

    @staticmethod
    def log_file_is_valid():
        assert isinstance(config.LOG_FILE, Path)
        assert config.LOG_FILE is not None
        assert config.LOG_FILE.exists()
        assert config.LOG_FILE.is_file()
        assert config.LOG_FILE.parent == config.LOG_DIR

    @staticmethod
    def exit_code_is_valid():
        assert config.EXIT_CODE.SUCCESS == 0
        assert config.EXIT_CODE.SYSTEM_ERROR == 1
        assert config.EXIT_CODE.VALIDATE_ERROR == 2
        assert config.EXIT_CODE.DATABASE_ERROR == 3


def test_required_config_attributes_exists():
    required = [
        'DB_PATH',
        'TABLE_NAME',
        'ALLOWED_TABLES_NAME',
        'REQUIREMENTS_HEADERS',
        'LOG_LEVEL',
        'LOG_DIR',
        'LOG_FILE',
        'EXIT_CODE'
    ]

    for attr in required:
        assert hasattr(config, attr)


def test_correctness_of_values():
    ConfigValidationHelper.db_path_is_valid()
    ConfigValidationHelper.table_name_is_valid()
    ConfigValidationHelper.allowed_tables_name_is_valid()
    ConfigValidationHelper.requirements_headers_is_valid()
    ConfigValidationHelper.log_level_is_valid()
    ConfigValidationHelper.log_dir_is_valid()
    ConfigValidationHelper.log_file_is_valid()
    ConfigValidationHelper.exit_code_is_valid()


def test_environments_isolation():
    assert base.ENV == 'base'
    assert base.LOG_LEVEL == 'INFO'

    assert prod.ENV == 'prod'
    assert prod.LOG_LEVEL == 'INFO'

    assert dev.ENV == 'dev'
    assert dev.LOG_LEVEL == 'DEBUG'