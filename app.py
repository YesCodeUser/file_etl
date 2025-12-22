import argparse
import json
import sys

from config import REQUIREMENTS_HEADERS, ExitCode

from validation.validator import Validation
from report.console_reporter import ConsoleReporter
from report.console_reporter_json import ConsoleReporterJSON
from storage.sqlite import Storage

def mode_logic():
    validate = Validation(args.file_path, REQUIREMENTS_HEADERS)
    result = validate.run()

    if args.dry_run and args.json:
        ConsoleReporterJSON.print_json_report(result)

        if result.system_error:
            sys.exit(ExitCode.SYSTEM_ERROR)
        elif result.errors:
            sys.exit(ExitCode.VALIDATE_ERROR)
        else:
            sys.exit(ExitCode.SUCCESS)

    elif args.dry_run or args.no_db:

        ConsoleReporter.print_data_report(result)

        if result.system_error:
            sys.exit(ExitCode.SYSTEM_ERROR)
        elif result.errors:
            sys.exit(ExitCode.VALIDATE_ERROR)
        else: sys.exit(ExitCode.SUCCESS)

    elif args.json:

        ConsoleReporterJSON.print_json_report(result)

        if result.system_error:
            sys.exit(ExitCode.SYSTEM_ERROR)
        elif result.errors:
            sys.exit(ExitCode.VALIDATE_ERROR)
        else:
            storage = Storage()
            storage.create_or_open_database()
            db_result = storage.data_save(result.valid_rows)

            print(json.dumps(db_result, indent=2, ensure_ascii=False))
            if db_result.get('error'):
                sys.exit(ExitCode.DATABASE_ERROR)
            else:
                sys.exit(ExitCode.SUCCESS)

    else:
        ConsoleReporter.print_data_report(result)

        if result.system_error:
            sys.exit(ExitCode.SYSTEM_ERROR)
        elif result.errors:
            sys.exit(ExitCode.VALIDATE_ERROR)
        else:
            storage = Storage()
            storage.create_or_open_database()
            db_result = storage.data_save(result.valid_rows)

        if db_result.get('error'):
            print(f'Error of saving in database: {db_result['error']}')
            sys.exit(ExitCode.DATABASE_ERROR)
        else:
            ConsoleReporter.print_db_statistics(db_result)
            sys.exit(ExitCode.SUCCESS)


parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files')

parser.add_argument('file_path', type=str, help='path to .csv file')
parser.add_argument('--dry-run', action='store_true', help='mode without database')
parser.add_argument('--no-db', action='store_true', help='mode without database')
parser.add_argument('--json', action='store_true', help='mode for output in JSON format')

args = parser.parse_args()

mode_logic()






