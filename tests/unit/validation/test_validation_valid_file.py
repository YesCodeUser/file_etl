from validation.validator import Validation
from config import REQUIREMENTS_HEADERS


def test_validation_with_valid_csv(tmp_path):
    csv_file = tmp_path / 'employees.csv'
    csv_file.write_text(
        'id,name,salary\n'
        '1,Aron.A,1000\n'
        '2,artem,2000.5\n'
        '3,Will Smith,100'
    )

    validator = Validation(csv_file, REQUIREMENTS_HEADERS)

    result = validator.run()

    print(f'ERRORS: {result.errors}')

    assert result.system_error is None
    assert result.errors == []
    assert result.amount_rows == 3
    assert result.amount_valid_rows == 3
    assert result.amount_invalid_rows == 0
