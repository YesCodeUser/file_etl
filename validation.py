import os
import sys
from csv import DictReader
from report import Report


class Validation:
    def __init__(self, file_path, requirements_headers=None):
        self.file_path = file_path
        self.valid_rows = []
        self.requirements_headers = requirements_headers
        self.unique_id = set()
        self.report = Report(file_path)

    def _is_file_empty(self):
        return os.path.getsize(self.file_path) == 0

    def run(self):
        try:
            self._validate_file()
        except(FileNotFoundError, IsADirectoryError, ValueError) as e:
            self.report.print_exception_report(e, 'System Error')
            sys.exit(1)

        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                self._validate_structure_file(file)
            except ValueError as e:
                self.report.print_exception_report(e, 'File Error')
                sys.exit(2)

            file.seek(0)
            reader = DictReader(file)

            for line_number, row in enumerate(reader, start=1):
                valid_id = self._validate_id(line_number, row['id'])
                valid_name = self._validate_name(line_number, row['name'])
                valid_salary = self._validate_salary(line_number, row['salary'])

                if None not in (valid_id, valid_name, valid_salary):
                    self.valid_rows.append({
                        'id': valid_id,
                        'name': valid_name,
                        'salary': valid_salary
                    })
                    self.report.amount_valid_rows += 1
                else:
                    self.report.amount_invalid_rows += 1

            self.report.amount_rows = line_number or 0

            if self.report.errors:
                self.report.print_data_report()
                sys.exit(2)
            else:
                self.report.print_data_report()

    def _validate_file(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'File {self.file_path} is not exists')

        if not os.path.isfile(self.file_path):
            raise IsADirectoryError(f'{self.file_path} is not file')

        if not self.file_path.endswith('.csv'):
            raise ValueError(f'File {self.file_path} is not .csv')

    def _validate_structure_file(self, file):
        lines = file.readlines()

        if not lines:
            raise ValueError(f'File {self.file_path} is empty')

        first_line = lines[0]
        for value in self.requirements_headers:
            if value not in first_line:
                raise ValueError(f'Column {value} is must be')

        if len(lines) == 1:
            raise ValueError(f'File {self.file_path} is empty after header')

    def _validate_id(self, line_number, id_data):
        if not id_data.strip():
            self.report.error_collector(line_number, 'id', 'id must be')
            return None

        try:
            id_data_int = int(id_data)
        except ValueError:
            self.report.error_collector(line_number, 'id', f'id {id_data} must be integer')
            return None

        if id_data_int <= 0:
            self.report.error_collector(line_number, 'id', f'id {id_data_int} must be > 0')
            return None

        if id_data_int not in self.unique_id:
            self.unique_id.add(id_data_int)
            return id_data_int
        else:
            self.report.error_collector(line_number, 'id', f'duplicate id {id_data_int}')

        return None

    def _validate_name(self, line_number, name_data):
        if not name_data.strip():
            self.report.error_collector(line_number, 'name', 'name must be')
            return None

        clean_name = name_data.replace(' ', '').replace('-', '').replace('.', '')
        if not clean_name.isalpha():
            self.report.error_collector(line_number, 'name', f'name {name_data} must be stroke')
            return None

        return name_data

    def _validate_salary(self, line_number, salary_data):
        if not salary_data.strip():
            self.report.error_collector(line_number, 'salary', 'salary must be')
            return None

        try:
            salary_data_float = float(salary_data.replace(',', '.'))
        except ValueError:
            self.report.error_collector(line_number, 'salary', f'salary {salary_data} must be float')
            return None

        if salary_data_float < 0:
            self.report.error_collector(line_number, 'salary', f'salary {salary_data_float} must be > 0')
            return None

        return salary_data_float
