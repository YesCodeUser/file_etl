from validation.validator import Validation
from config import REQUIREMENTS_HEADERS


def test_validation_id_is_missing(file):
    file.write_text(
        'id,name,salary\n'
        ',artem,100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'id'


def test_validation_id_is_not_int(file):
    file.write_text(
        'id,name,salary\n'
        'ff,artem,100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'id'


def test_validation_id_less_than_one(file):
    file.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'id'


def test_validation_id_is_not_unique(file):
    file.write_text(
        'id,name,salary\n'
        '1,artem,100\n'
        '1,john,1000'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'id'


def test_validation_name_is_missing(file):
    file.write_text(
        'id,name,salary\n'
        '1,,100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'name'


def test_validation_name_is_not_str(file):
    file.write_text(
        'id,name,salary\n'
        '1,30,100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'name'


def test_validation_salary_is_missing(file):
    file.write_text(
        'id,name,salary\n'
        '1,artem,'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'salary'


def test_validation_salary_is_not_float(file):
    file.write_text(
        'id,name,salary\n'
        '1,artem,ff'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'salary'


def test_validation_salary_less_than_zero(file):
    file.write_text(
        'id,name,salary\n'
        '1,artem,-100'
    )

    validator = Validation(file, REQUIREMENTS_HEADERS)
    result = validator.run()

    assert len(result.errors) == 1
    assert result.errors[0]['column'] == 'salary'
