from config import EXIT_CODE
from app import select_reporter
from report.console_reporter import ConsoleReporter
from report.console_reporter_json import ConsoleReporterJSON


def test_default_validate_data_error(file_csv, storage, application, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.errors != []

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporter


def test_default_validate_system_error(file_txt, storage, application, mock_args):
    file_txt.write_text('')

    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporter


def test_no_db_validate_data_error(file_csv, storage, application, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.errors != []

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporter


def test_no_db_validate_system_error(file_txt, storage, application, mock_args):
    file_txt.write_text('')

    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporter


def test_json_validate_data_error(file_csv, storage, application, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.json = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.errors != []

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporterJSON


def test_json_validate_system_error(file_txt, storage, application, mock_args):
    file_txt.write_text('')

    mock_args.json = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporterJSON


def test_json_no_db_validate_data_error(file_csv, storage, application, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.json = True
    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.errors != []

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporterJSON


def test_json_no_db_validate_system_error(file_txt, storage, application, mock_args):
    file_txt.write_text('')

    mock_args.json = True
    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application.run(args)
    report = select_reporter(args)

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None
    assert storage.connection is None

    assert report == ConsoleReporterJSON
