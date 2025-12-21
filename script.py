import argparse
import sys

from validation import Validation
from report import ConsoleReporter
from storage import Storage


parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files')
parser.add_argument('file_path', type=str, help='path to .csv file')
args = parser.parse_args()

requirements_headers = ['id', 'name', 'salary']


validate = Validation(args.file_path, requirements_headers)
result = validate.run()

ConsoleReporter.print_data_report(result)

if result.system_error:
    sys.exit(1)
elif result.errors:
    sys.exit(2)
else:
    storage = Storage()
    storage.create_or_open_database()
    db_result = storage.data_save(result.valid_rows)

    if db_result.get('error'):
        print(f'Error of saving in database: {db_result['error']}')
        sys.exit(3)
    else:
        ConsoleReporter.print_db_statistics(db_result)
        sys.exit(0)




