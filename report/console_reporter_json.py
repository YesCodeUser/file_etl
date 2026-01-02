import json
from datetime import datetime
from core.validation_result import ValidationResult
from core.storage_result import StorageResult


class ConsoleReporterJSON:
    def __init__(self):
        self.json_data = {}
        self.json_system_error = {}

    def _generate_json_report(self, result: ValidationResult):
        self.json_data = {
            'main_info': {
                'status': result.status,
                'file': result.file_path,
                'datetime': str(result.processed_at)
            },
            'statistics': {
                'amount_rows': result.amount_rows,
                'amount_valid_rows': result.amount_valid_rows,
                'amount_invalid_rows': result.amount_invalid_rows
            },
            'errors': result.errors
        }
        return self.json_data

    @staticmethod
    def _prepare_generate_json_report(result: ValidationResult):
        if result.amount_rows == result.amount_valid_rows:
            result.status = 'all valid'
        elif result.amount_valid_rows == 0:
            result.status = 'all invalid'
        else:
            result.status = 'partially valid'

    def _generate_json_system_error_report(self, result: ValidationResult):
        result.status = 'system_error'

        self.json_system_error = {
            'type': type(result.system_error).__name__,
            'message': str(result.system_error),
            'file': result.file_path,
            'date_time': datetime.now().strftime("%d.%m.%Y %H:%M")
        }

    def _print_json_system_error_report(self, result: ValidationResult):
        self._generate_json_system_error_report(result)

        print(json.dumps(self.json_system_error, indent=2, ensure_ascii=False))

    def print_report(self, result: ValidationResult, db_result=None):
        if result.system_error:
            self._print_json_system_error_report(result)
            return

        ConsoleReporterJSON._prepare_generate_json_report(result)
        json_data = self._generate_json_report(result)
        print(json.dumps(json_data, indent=2, ensure_ascii=False))

        if db_result is not None:
            json_db_report = ConsoleReporterJSON._generate_json_db_result(db_result)
            print(json.dumps(json_db_report, indent=2, ensure_ascii=False))

    @staticmethod
    def _generate_json_db_result(db_result: StorageResult):
        json_db_result = db_result.database_result.copy()
        if db_result.database_error:
            json_db_result['error'] = str(db_result.database_error)
        return json_db_result



