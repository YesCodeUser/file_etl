from pathlib import Path
import config

class ConfigValidationHelper:

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
        'REQUIREMENTS_HEADERS',
        'LOG_LEVEL',
        'LOG_DIR',
        'LOG_FILE',
        'EXIT_CODE'
    ]

    for attr in required:
        assert hasattr(config, attr)


def test_correctness_of_values():
    ConfigValidationHelper.requirements_headers_is_valid()
    ConfigValidationHelper.log_level_is_valid()
    ConfigValidationHelper.log_dir_is_valid()
    ConfigValidationHelper.log_file_is_valid()
    ConfigValidationHelper.exit_code_is_valid()

