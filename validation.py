import os
from csv import DictReader
from report import ProcessingResult


class Validation:
    def __init__(self, file_path, requirements_headers=None):
        self.file_path = file_path
        self.requirements_headers = requirements_headers
        self.unique_id = set()
        self.result = ProcessingResult(file_path)

    def _is_file_empty(self):
        return os.path.getsize(self.file_path) == 0

    def run(self):
        try:
            self._validate_file()
        except(FileNotFoundError, IsADirectoryError, ValueError) as e:
            self.result.system_error = e
            return self.result

        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                self._validate_structure_file(file)
            except ValueError as e:
                self.result.system_error = e
                return self.result

            file.seek(0)
            reader = DictReader(file)

            for line_number, row in enumerate(reader, start=1):
                valid_id = self._validate_id(line_number, row['id'])
                valid_name = self._validate_name(line_number, row['name'])
                valid_salary = self._validate_salary(line_number, row['salary'])

                if None not in (valid_id, valid_name, valid_salary):
                    self.result.valid_rows.append({
                        'id': valid_id,
                        'name': valid_name,
                        'salary': valid_salary
                    })
                    self.result.amount_valid_rows += 1
                else:
                    self.result.amount_invalid_rows += 1

            self.result.amount_rows = line_number or 0

        return self.result

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
            self.result.errors.append({
                'line': line_number,
                'column': 'id',
                'error': 'data id must be'
            })
            return None

        try:
            id_data_int = int(id_data)
        except ValueError:
            self.result.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'id {id_data} must be integer'
            })
            return None

        if id_data_int <= 0:
            self.result.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'id {id_data_int} must be > 0'
            })
            return None

        if id_data_int not in self.unique_id:
            self.unique_id.add(id_data_int)
            return id_data_int
        else:
            self.result.errors.append({
                'line': line_number,
                'column': 'id',
                'error': f'duplicate id {id_data_int}'
            })

        return None

    def _validate_name(self, line_number, name_data):
        if not name_data.strip():
            self.result.errors.append({
                'line': line_number,
                'column': 'name',
                'error': 'data name must be'
            })

            return None

        clean_name = name_data.replace(' ', '').replace('-', '').replace('.', '')
        if not clean_name.isalpha():
            self.result.errors.append({
                'line': line_number,
                'column': 'name',
                'error': f'name {name_data} must be stroke'
            })
            return None

        return name_data

    def _validate_salary(self, line_number, salary_data):
        if not salary_data.strip():
            self.result.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': 'data salary must be'
            })

            return None

        try:
            salary_data_float = float(salary_data.replace(',', '.'))
        except ValueError:
            self.result.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': f'salary {salary_data} must be float'
            })
            return None

        if salary_data_float < 0:
            self.result.errors.append({
                'line': line_number,
                'column': 'salary',
                'error': f'salary {salary_data_float} must be > 0'
            })
            return None

        return salary_data_float
