from validation.validator import Validation
from config import REQUIREMENTS_HEADERS


def test_validation_file_not_found():
    validator = Validation('not_exists.csv', REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, FileNotFoundError)


def test_validation_file_is_dir(tmp_path):
    directory = tmp_path / 'core/'
    directory.mkdir()
    validator = Validation(directory, REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, IsADirectoryError)


def test_validation_file_wrong_extension(file_txt):
    file_txt.write_text('hello')

    validator = Validation(file_txt, REQUIREMENTS_HEADERS)

    result = validator.run()

    assert isinstance(result.system_error, ValueError)
    assert '.csv' in str(result.system_error)


def test_validation_file_is_empty(file_csv):
    file_csv.write_text('')

    validator = Validation(file_csv, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert isinstance(result.system_error, ValueError)


def test_validation_required_field_is_missing(file_csv):
    file_csv.write_text('id,name')

    validator = Validation(file_csv, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert isinstance(result.system_error, ValueError)


def test_validation_file_is_empty_after_header(file_csv):
    file_csv.write_text('id,name,salary')

    validator = Validation(file_csv, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert isinstance(result.system_error, ValueError)
