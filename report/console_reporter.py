from datetime import datetime

from core.storage_result import StorageResult
from core.validation_result import ValidationResult


class ConsoleReporter:
    def __init__(self):
        self.report = {}
        self.system_error_report = {}

    @staticmethod
    def _prepare_to_generate_data_report(result: ValidationResult):
        if result.amount_rows == result.amount_valid_rows:
            result.status = 'all valid'
        elif result.amount_valid_rows == 0:
            result.status = 'all invalid'
        else:
            result.status = 'partially valid'

    def _generate_data_report(self, result: ValidationResult):
        ConsoleReporter._prepare_to_generate_data_report(result)
        self.report = {
            'main_info': {
                'status': result.status,
                'file': result.file_path,
                'datetime': result.processed_at
            },
            'statistics': {
                'amount_rows': result.amount_rows,
                'amount_valid_rows': result.amount_valid_rows,
                'amount_invalid_rows': result.amount_invalid_rows
            },
            'errors': result.errors
        }

    def print_report(self, result: ValidationResult, db_result=None):
        if result.system_error:
            self._print_system_error_report(result)
            return

        self._generate_data_report(result)

        print('📊 REPORT:')
        print('-' * 20)
        print('📋 Main Info:')
        print(f'Status: {self.report['main_info']['status']}')
        print(f'File: {self.report["main_info"]["file"]}')
        print(f'Date & Time: {self.report['main_info']['datetime']}')
        print('-' * 20)
        print('📈 Statistics')
        print(f'Amount rows: {self.report['statistics']['amount_rows']}')
        print(f'Valid rows: {self.report['statistics']['amount_valid_rows']}')
        print(f'Invalid rows: {self.report['statistics']['amount_invalid_rows']}')
        if result.errors:
            ConsoleReporter._print_data_error(result)

        if db_result:
            ConsoleReporter._print_db_statistics(db_result)

    def _generate_system_error_report(self, result: ValidationResult):
        result.status = 'system_error'

        self.system_error_report = {
            'type': type(result.system_error).__name__,
            'message': str(result.system_error),
            'file': result.file_path,
            'date_time': datetime.now().strftime("%d.%m.%Y %H:%M")
        }

    def _print_system_error_report(self, result: ValidationResult):
        self._generate_system_error_report(result)

        print('🚫 SYSTEM ERROR REPORT:')
        print('-' * 20)
        print(f'Type: {self.system_error_report['type']}')
        print(f'Message: {self.system_error_report['message']}')
        print(f'File: {self.system_error_report['file']}')
        print(f'Date & Time: {self.system_error_report['date_time']}')

    @staticmethod
    def _print_data_error(result: ValidationResult):
        print('-' * 20)
        print('🚫Errors: \n')
        for dictionary in result.errors:
            for key, value in dictionary.items():
                print(f'{key}: {dictionary[key]}')
            print('-' * 20)

    def _print_success_validate(self):
        print('✅ DATA SUCCESS REPORT:')
        print('-' * 20)
        print('📋 Main Info:')
        print(f'Status: {self.report['main_info']['status']}')
        print(f'File: {self.report['main_info']['file']}')
        print(f'Date & Time: {self.report['main_info']['datetime']}')

    @staticmethod
    def _print_db_statistics(db_result: StorageResult):
        print('-' * 20)
        print('📊 RESULT OF SAVING IN DATABASE')
        print('-' * 20)
        print(f'📤 Accepted lines: {db_result.database_result['attempted']}')
        print(f'✅ Saved lines: {db_result.database_result['inserted']}')
        print(f'⚠️ Ignored lines: {db_result.database_result['ignored']}')
