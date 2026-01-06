from config import EXIT_CODE
from app import select_reporter
from report.console_reporter import ConsoleReporter
from report.console_reporter_json import ConsoleReporterJSON


def test_default_validate_data_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporter)

    reporter.print_report(validation_result, db_result)
    report = reporter.report

    assert report['main_info']['status'] == 'all invalid'
    assert report['main_info']['file'] == str(file_csv)
    assert report['main_info']['datetime']
    assert report['statistics']['amount_rows'] == 1
    assert report['statistics']['amount_valid_rows'] == 0
    assert report['statistics']['amount_invalid_rows'] == 1
    assert report['errors'] != []


def test_default_validate_system_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text('')

    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    reporter.print_report(validation_result)

    system_error_report = reporter.system_error_report

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporter)

    assert system_error_report['type'] == 'EmptyDataError'
    assert isinstance(system_error_report['message'], str)
    assert system_error_report['file'] == str(file_csv)
    assert system_error_report['date_time']


def test_no_db_validate_data_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporter)

    reporter.print_report(validation_result, db_result)
    report = reporter.report

    assert report['main_info']['status'] == 'all invalid'
    assert report['main_info']['file'] == str(file_csv)
    assert report['main_info']['datetime']
    assert report['statistics']['amount_rows'] == 1
    assert report['statistics']['amount_valid_rows'] == 0
    assert report['statistics']['amount_invalid_rows'] == 1
    assert report['errors'] != []


def test_no_db_validate_system_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text('')

    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)

    reporter = select_reporter(args)
    reporter.print_report(validation_result)

    system_error_report = reporter.system_error_report

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporter)

    assert system_error_report['type'] == 'EmptyDataError'
    assert isinstance(system_error_report['message'], str)
    assert system_error_report['file'] == str(file_csv)
    assert system_error_report['date_time']


def test_json_validate_data_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.json = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    reporter.print_report(validation_result)

    json_system_errors = reporter.json_system_error

    assert json_system_errors == {}

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporterJSON)

    reporter.print_report(validation_result, db_result)
    report = reporter.json_data

    assert report['main_info']['status'] == 'all invalid'
    assert report['main_info']['file'] == str(file_csv)
    assert report['main_info']['datetime']
    assert report['statistics']['amount_rows'] == 1
    assert report['statistics']['amount_valid_rows'] == 0
    assert report['statistics']['amount_invalid_rows'] == 1
    assert report['errors'] != []


def test_json_validate_system_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text('')

    mock_args.json = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    reporter.print_report(validation_result)
    json_system_error = reporter.json_system_error

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporterJSON)

    assert json_system_error['type'] == 'EmptyDataError'
    assert isinstance(json_system_error['message'], str)
    assert json_system_error['file'] == str(file_csv)
    assert json_system_error['date_time']


def test_json_no_db_validate_data_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text(
        'id,name,salary\n'
        '0,artem,100'
    )

    mock_args.json = True
    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)

    assert validation_result.errors != []

    assert exit_code == EXIT_CODE.VALIDATE_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporterJSON)


def test_json_no_db_validate_system_error(file_csv, storage, application_no_db, mock_args):
    file_csv.write_text('')

    mock_args.json = True
    mock_args.no_db = True
    args = mock_args

    validation_result, exit_code, db_result = application_no_db.run(args)
    reporter = select_reporter(args)
    reporter.print_report(validation_result)

    json_system_error = reporter.json_system_error

    assert validation_result.system_error is not None

    assert exit_code == EXIT_CODE.SYSTEM_ERROR

    assert db_result is None

    assert isinstance(reporter, ConsoleReporterJSON)

    assert json_system_error['type'] == 'EmptyDataError'
    assert isinstance(json_system_error['message'], str)
    assert json_system_error['file'] == str(file_csv)
    assert json_system_error['date_time']
