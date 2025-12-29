import argparse
import sys

from logs.logs import setup_logging
from config import REQUIREMENTS_HEADERS
from core.application import Application
from report.console_reporter import ConsoleReporter
from report.console_reporter_json import ConsoleReporterJSON


def parse_argument():
    parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files')
    parser.add_argument('file_path', type=str, help='path to .csv file')
    parser.add_argument('--no-db', action='store_true', help='mode without database')
    parser.add_argument('--json', action='store_true', help='mode for output in JSON format')
    return parser.parse_args()


def select_reporter(args):
    if args.json:
        return ConsoleReporterJSON
    else:
        return ConsoleReporter


def main():
    setup_logging()

    args = parse_argument()

    application = Application(args.file_path, REQUIREMENTS_HEADERS)
    validation_result, exit_code, db_result = application.run(args)
    reporter = select_reporter(args)
    reporter.print_report(validation_result, db_result)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
