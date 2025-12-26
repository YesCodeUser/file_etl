import json
from core.validation_result import ValidationResult


class ConsoleReporterJSON:
    @staticmethod
    def _generate_json_report(result: ValidationResult):
            json_data = {
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
            return json_data

    @staticmethod
    def _prepare_generate_json_report(result: ValidationResult):
            if result.system_error:
                result.status = 'System Error'
                return

            if result.amount_rows == result.amount_valid_rows:
                result.status = 'all valid'
            elif result.amount_valid_rows == 0:
                result.status = 'all invalid'
            else:
                result.status = 'partially valid'



    @staticmethod
    def print_json_report(result: ValidationResult, db_result = None):
        ConsoleReporterJSON._prepare_generate_json_report(result)
        json_data = ConsoleReporterJSON._generate_json_report(result)
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
        if db_result is not None:
            if db_result.database_error:
                print(json.dumps(db_result.database_error))
            else:
                print(json.dumps(db_result.database_result, indent=2, ensure_ascii=False))