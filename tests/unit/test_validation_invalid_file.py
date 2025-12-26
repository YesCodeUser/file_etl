from validation.validator import Validation
from config import REQUIREMENTS_HEADERS


def test_validation_file_not_found():
    validator = Validation('not_exists.csv', REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, FileNotFoundError)


def test_validation_file_is_dir():
    validator = Validation('core/', REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, IsADirectoryError)


def test_validation_file_wrong_extension(tmp_path):
    file = tmp_path / 'data.txt'
    file.write_text('hello')

    validator = Validation(file, REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, ValueError)
    assert '.csv' in str(result.system_error)


def test_validation_file_is_empty(tmp_path):
    file = tmp_path / 'data.csv'
    file.write_text('')

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert isinstance(result.system_error, ValueError)


def test_validation_required_field_is_missing(tmp_path):
    file = tmp_path / 'data.csv'
    file.write_text('id,name')

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert isinstance(result.system_error, ValueError)


def test_validation_file_is_empty_after_header(tmp_path):
    file = tmp_path / 'data.csv'
    file.write_text('id,name,salary')

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    print(str(result.system_error))

    assert isinstance(result.system_error, ValueError)
