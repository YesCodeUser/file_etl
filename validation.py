import os
import sys
from csv import DictReader


class Validation:
    def __init__(self, requirements_headers=None):
        self.errors = []
        self.valid_rows = []
        self.requirements_headers = requirements_headers
        self.unique_id = set()

    @staticmethod
    def is_file_empty(file_path):
        return os.path.getsize(file_path) == 0

    def run(self, file_path):
        try:
            self.validate_file(file_path)
        except(FileNotFoundError, IsADirectoryError, ValueError) as e:
            print(f'error: {e}')
            sys.exit(1)

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                self.validate_structure_file(file)
            except ValueError as e:
                print(f'error: {e}')
                sys.exit(1)
            file.seek(0)
            reader = DictReader(file)

            for line_number, row in enumerate(reader, start=1):
                valid_id = self.validate_id(line_number, row['id'])
                valid_name = self.validate_name(line_number, row['name'])
                valid_salary = self.validate_salary(line_number, row['salary'])

                if None not in (valid_id, valid_name, valid_salary):
                    self.valid_rows.append({
                        'id': valid_id,
                        'name': valid_name,
                        'salary': valid_salary
                    })

            if self.errors:
                self.print_errors()
                sys.exit(1)
            else:
                pass


    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} is not found')

        if not os.path.isfile(file_path):
            raise IsADirectoryError(f'{file_path} is not file')

        if not file_path.endswith('.csv'):
            raise ValueError(f'{file_path} is not .csv file')

        if self.is_file_empty(file_path):
            raise ValueError(f'{file_path} is empty')

    def validate_structure_file(self, file):
        first_line = file.readline()
        for value in self.requirements_headers:
            if value not in first_line:
                raise ValueError(f'column {value} is must be')

    def validate_id(self, line_number, id_data):
        if not id_data.strip():
            self.errors.append({
                'line': line_number,
                'column': 'id',
                'error': 'id must be'
            })
            return None

        try:
            id_data_int = int(id_data)
        except ValueError:
            self.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'id {id_data} must be integer'
            })
            return None

        if id_data_int <= 0:
            self.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'id {id_data_int} must be > 0'
            })
            return None

        if id_data_int not in self.unique_id:
            self.unique_id.add(id_data_int)
            return id_data_int
        else:
            self.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'duplicate id {id_data_int}'
            })

        return None

    def validate_name(self, line_number, name_data):
        if not name_data.strip():
            self.errors.append({
                'line': line_number,
                'column': 'name',
                'error': f'name must be'
            })
            return None
        clean_name = name_data.replace(' ', '').replace('-', '').replace('.', '')
        if not clean_name.isalpha():
            self.errors.append({
                'line': line_number,
                'column': 'name',
                'error': f'name {name_data} must be stroke'
            })
            return None

        return name_data

    def validate_salary(self, line_number, salary_data):
        if not salary_data.strip():
            self.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': f'salary must be'
            })
            return None

        try:
            salary_data_float = float(salary_data.replace(',', '.'))
        except ValueError:
            self.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': f'salary {salary_data} must be float'
            })
            return None

        if salary_data_float < 0:
            self.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': f'salary {salary_data_float} must be > 0'
            })
            return None

        return salary_data_float

    def print_errors(self):
        print('errors:')
        for dictionary in self.errors:
            for key, value in dictionary.items():
                print(f'{key}: {dictionary[key]}')
            print('-' * 20)
