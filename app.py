import argparse
import sys

from core.application import Application
from config import REQUIREMENTS_HEADERS
from report.console_reporter import ConsoleReporter
from report.console_reporter_json import ConsoleReporterJSON

def select_reporter(valid_result, database_result):
    if args.json:
        return ConsoleReporterJSON.print_json_report(valid_result, database_result)
    else:
        return ConsoleReporter.print_data_report(valid_result, database_result)

parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files')

parser.add_argument('file_path', type=str, help='path to .csv file')
parser.add_argument('--dry-run', action='store_true', help='mode without database')
parser.add_argument('--no-db', action='store_true', help='mode without database')
parser.add_argument('--json', action='store_true', help='mode for output in JSON format')

args = parser.parse_args()

application = Application(args.file_path, REQUIREMENTS_HEADERS)
validation_result, exit_code, db_result = application.run(args)
reporter = select_reporter(validation_result, db_result)
sys.exit(exit_code)






