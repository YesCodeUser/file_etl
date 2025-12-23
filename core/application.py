from validation.validator import Validation
from core.validation_result import ValidationResult
from config import ExitCode
from storage.sqlite import Storage


class Application:
    def __init__(self, file_path, requirements_headers=None):
        self.file_path = file_path
        self.requirements_headers = requirements_headers
        self.validator = Validation(file_path, requirements_headers)

    def run(self, args):
        validation_result = self.validator.run()

        if Application._has_system_error(validation_result):
            return validation_result, ExitCode.SYSTEM_ERROR, None

        if Application._has_validate_error(validation_result):
            return validation_result, ExitCode.VALIDATE_ERROR, None

        result = Application.mode_logic(args, validation_result)

        return result

    @staticmethod
    def _has_system_error(validation_result: ValidationResult):
        if validation_result.system_error:
            return True
        return False

    @staticmethod
    def _has_validate_error(validation_result: ValidationResult):
        if validation_result.errors:
            return True
        return False

    @staticmethod
    def mode_logic(args, validation_result):
        if (args.dry_run or args.no_db) and args.json:
            return validation_result, ExitCode.SUCCESS, None

        elif args.dry_run or args.no_db:
            return validation_result, ExitCode.SUCCESS, None

        else:
            storage = Storage()
            storage.create_or_open_database()
            db_result = storage.data_save(validation_result.valid_rows)
            storage.close()
            if db_result.get('error'):
                return validation_result, ExitCode.DATABASE_ERROR, db_result
            else:
                return validation_result, ExitCode.SUCCESS, db_result


