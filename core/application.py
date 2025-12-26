import logging
from validation.validator import Validation
from core.validation_result import ValidationResult
from config import EXIT_CODE, DB_PATH
from storage.sqlite import Storage

logger = logging.getLogger(__name__)

class Application:
    def __init__(self, file_path, requirements_headers=None):
        self.file_path = file_path
        self.requirements_headers = requirements_headers
        self.validator = Validation(file_path, requirements_headers)

    def run(self, args):
        validation_result = self.validator.run()

        if Application._has_system_error(validation_result):
            logger.critical(f'Validation system error: {validation_result.system_error}',
                extra={
                    'file': validation_result.file_path,
                    'error_type': type(validation_result.system_error).__name__,
                    'error': str(validation_result.system_error)
                }
            )
            return validation_result, EXIT_CODE.SYSTEM_ERROR, None

        if Application._has_validate_error(validation_result):
            logger.warning(f'Validation finished with errors. File: {validation_result.file_path}',
                extra={
                    'file': validation_result.file_path,
                    'error': validation_result.errors
                }
            )
            return validation_result, EXIT_CODE.VALIDATE_ERROR, None
        logger.info(f'Validation is successful. File: {validation_result.file_path}')

        result = Application.mode_logic(args, validation_result, )
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
            return validation_result, EXIT_CODE.SUCCESS, None

        elif args.dry_run or args.no_db:
            return validation_result, EXIT_CODE.SUCCESS, None

        else:
            storage = Storage(DB_PATH)
            db_result = storage.run(validation_result.valid_rows)
            if db_result.database_error:
                return validation_result, EXIT_CODE.DATABASE_ERROR, db_result
            else:
                return validation_result, EXIT_CODE.SUCCESS, db_result


