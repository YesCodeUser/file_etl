from datetime import datetime


class Report:
    def __init__(self, file_path):
        self.file_path = file_path
        self.report = {}
        self.errors = []
        self.amount_rows = 0
        self.amount_errors = 0
        self.amount_valid_rows = 0
        self.amount_invalid_rows = 0
        self.status = ''

    def _prepare_to_generate_data_report(self):
        if self.amount_rows == self.amount_valid_rows:
            self.status = 'all valid'
        elif self.amount_valid_rows == 0:
            self.status = 'all invalid'
        else:
            self.status = 'partially valid'

    def _generate_data_report(self, ):
        self._prepare_to_generate_data_report()
        self.report = {
            'main info': {
                'status': self.status,
                'file': self.file_path,
                'datetime': datetime.now().strftime('%d.%m.%Y %H:%M')
            },
            'statistics': {
                'amount_rows': self.amount_rows,
                'amount_valid_rows': self.amount_valid_rows,
                'amount_invalid_rows': self.amount_invalid_rows
            },
            'errors': self.errors
        }

    def print_data_report(self):
        self._generate_data_report()
        print('📊 REPORT:')
        print('-' * 20)
        print('📋 Main Info:')
        print(f'Status: {self.report['main info']['status']}')
        print(f'File: {self.report['main info']['file']}')
        print(f'Date & Time: {self.report['main info']['datetime']}')
        print('-' * 20)
        print('📈 Statistics')
        print(f'Amount rows: {self.report['statistics']['amount_rows']}')
        print(f'Valid rows: {self.report['statistics']['amount_valid_rows']}')
        print(f'Invalid rows: {self.report['statistics']['amount_invalid_rows']}')
        if self.errors:
            print('-' * 20)
            print('🚫Errors:')
            for dictionary in self.errors:
                for key, value in dictionary.items():
                    print(f'{key}: {dictionary[key]}')

    def print_exception_report(self, exception, error_name):
        print(f'🚫 {error_name}')
        print('-' * 20)
        print(f'Type: {type(exception).__name__}')
        print(f'Message: {str(exception)}')
        print(f'File: {self.file_path}')
        print(f'Date & Time: {datetime.now().strftime('%d.%m.%Y %H:%M')}')

    def print_universal_report(self, error_name, error_text):
        print(f'🚫 {error_name}')
        print('-' * 20)
        print(f'Message: {error_text}')
        print(f'File: {self.file_path}')
        print(f'Date & Time: {datetime.now().strftime('%d.%m.%Y %H:%M')}')

    def error_collector(self, line, column, error_text):
        self.errors.append({
            'line': line,
            'column': column,
            'error': error_text
        })
