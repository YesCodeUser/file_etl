import argparse
from validation import Validation

parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files')

parser.add_argument('file_path', type=str, help='path to .csv file')

args = parser.parse_args()

requirements_headers = ['id', 'name', 'salary']


validate = Validation(requirements_headers)
validate.run(args.file_path)
