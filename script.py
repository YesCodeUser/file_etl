import argparse
import sys
from csv import DictReader
from functions import validate_file

parser = argparse.ArgumentParser(description='The script is used to retrieve and validate data from csv files.')

parser.add_argument('file_path', type=str, help='path to .csv file')

args = parser.parse_args()

try:
    if validate_file(args.file_path):
        with open(args.file_path, 'r', encoding='utf-8') as file:
            reader = DictReader(file)
            for row in reader:
                print(row)

except (FileNotFoundError, IsADirectoryError, ValueError) as e:
    print(f'Error: {e}')
    sys.exit(1)
