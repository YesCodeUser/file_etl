import argparse
import sys

from validation import Validation
from report import ConsoleReporter


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
    sys.exit(0)
