from config import EXIT_CODE
from report.console_reporter_json import ConsoleReporterJSON
from report.console_reporter import ConsoleReporter
from app import select_reporter


def test_default_app_success(file_csv, db_path, application, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '1,andrey,1000\n'
        '2,john,200'
    )

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    reporter = select_reporter(args)

    assert validation_result.errors == []
    assert validation_result.system_error is None
    assert len(validation_result.valid_rows) == 2
    assert validation_result.amount_rows == 2
    assert validation_result.amount_valid_rows == 2
    assert validation_result.amount_invalid_rows == 0

    assert exit_code == EXIT_CODE.SUCCESS

    assert db_result.database_error is None
    assert db_result.database_result['attempted'] == 2
    assert db_result.database_result['ignored'] == 0
    assert db_result.database_result['inserted'] == 2

    assert reporter == ConsoleReporter


def test_no_db_app_success(file_csv, mock_args, application, storage):
    file_csv.write_text(
        'id,name,salary\n'
        '1,artem,1000'
    )
    mock_args.no_db = True

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    reporter = select_reporter(args)

    assert validation_result.errors == []
    assert validation_result.system_error is None
    assert len(validation_result.valid_rows) == 1
    assert validation_result.amount_rows == 1
    assert validation_result.amount_valid_rows == 1
    assert validation_result.amount_invalid_rows == 0

    assert exit_code == EXIT_CODE.SUCCESS

    assert db_result is None
    assert storage.connection is None

    assert reporter == ConsoleReporter


def test_json_app_success(file_csv, mock_args, application):
    file_csv.write_text(
        'id,name,salary\n'
        '1,artem,200'
    )

    mock_args.json = True

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    reporter = select_reporter(args)

    assert validation_result.errors == []
    assert validation_result.system_error is None
    assert len(validation_result.valid_rows) == 1
    assert validation_result.amount_rows == 1
    assert validation_result.amount_valid_rows == 1
    assert validation_result.amount_invalid_rows == 0

    assert exit_code == EXIT_CODE.SUCCESS

    assert db_result.database_error is None
    assert db_result.database_result['attempted'] == 1
    assert db_result.database_result['ignored'] == 0
    assert db_result.database_result['inserted'] == 1

    assert reporter == ConsoleReporterJSON


def test_no_db_json_app_success(file_csv, mock_args, application, storage):
    file_csv.write_text(
        'id,name,salary\n'
        '1,artem,1000'
    )
    mock_args.no_db = True
    mock_args.json = True

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    reporter = select_reporter(args)

    assert validation_result.errors == []
    assert validation_result.system_error is None
    assert len(validation_result.valid_rows) == 1
    assert validation_result.amount_rows == 1
    assert validation_result.amount_valid_rows == 1
    assert validation_result.amount_invalid_rows == 0

    assert exit_code == EXIT_CODE.SUCCESS

    assert db_result is None
    assert storage.connection is None

    assert reporter == ConsoleReporterJSON