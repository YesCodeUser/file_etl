from datetime import datetime


class ProcessingResult:
    def __init__(self, file_path):
        self.file_path = file_path
        self.system_error = None

        self.report = {}
        self.errors = []
        self.valid_rows = []

        self.amount_rows = 0
        self.amount_valid_rows = 0
        self.amount_invalid_rows = 0
        self.status = ''
        self.processed_at = datetime.now().strftime('%d.%m.%Y %H:%M')


class ConsoleReporter:
    @staticmethod
    def _prepare_to_generate_data_report(result: ProcessingResult):
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
    def _generate_data_report(result: ProcessingResult):
        ConsoleReporter._prepare_to_generate_data_report(result)
        result.report = {
            'main info': {
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

    @staticmethod
    def print_data_report(result: ProcessingResult):
        if result.system_error:
            ConsoleReporter._print_system_error_report(result)
            return

        ConsoleReporter._generate_data_report(result)

        if result.status == 'all valid':
            ConsoleReporter._print_success_validate(result)
            return

        print('📊 REPORT:')
        print('-' * 20)
        print('📋 Main Info:')
        print(f'Status: {result.report['main info']['status']}')
        print(f'File: {result.report['main info']['file']}')
        print(f'Date & Time: {result.report['main info']['datetime']}')
        print('-' * 20)
        print('📈 Statistics')
        print(f'Amount rows: {result.report['statistics']['amount_rows']}')
        print(f'Valid rows: {result.report['statistics']['amount_valid_rows']}')
        print(f'Invalid rows: {result.report['statistics']['amount_invalid_rows']}')
        if result.errors:
            ConsoleReporter._print_data_error(result)

    @staticmethod
    def _print_system_error_report(result: ProcessingResult):
        print('🚫 SYSTEM ERROR REPORT:')
        print('-' * 20)
        print(f'Type: {type(result.system_error).__name__}')
        print(f'Message: {str(result.system_error)}')
        print(f'File: {result.file_path}')
        print(f'Date & Time: {datetime.now().strftime("%d.%m.%Y %H:%M")}')

    @staticmethod
    def _print_data_error(result: ProcessingResult):
        print('-' * 20)
        print('🚫Errors: \n')
        for dictionary in result.errors:
            for key, value in dictionary.items():
                print(f'{key}: {dictionary[key]}')
            print('-' * 20)

    @staticmethod
    def _print_success_validate(result: ProcessingResult):
        print('✅ DATA SUCCESS REPORT:')
        print('-' * 20)
        print('📋 Main Info:')
        print(f'Status: {result.report['main info']['status']}')
        print(f'File: {result.report['main info']['file']}')
        print(f'Date & Time: {result.report['main info']['datetime']}')

    @staticmethod
    def print_db_statistics(db_result):
        print('-' * 20)
        print('📊 RESULT OF SAVING IN DATABASE')
        print('-' * 20)
        print(f'📤 Accepted lines: {db_result['attempted']}')
        print(f'✅ Saved lines: {db_result['inserted']}')
        print(f'⚠️ Ignored lines: {db_result['ignored']}')












