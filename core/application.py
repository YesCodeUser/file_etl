import logging
from validation.validator import Validation
from core.validation_result import ValidationResult
from config import EXIT_CODE
from storage.postgres import PostgresStorage

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, file_path,  requirements_headers=None, storage=None,):
        self.file_path = file_path
        self.storage = storage
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
            logger.error(f'Validation finished with errors. File: {validation_result.file_path}',
                         extra={
                             'file': validation_result.file_path,
                             'error': validation_result.errors
                         }
                         )
            return validation_result, EXIT_CODE.VALIDATE_ERROR, None
        logger.info(f'Validation is successful. File: {validation_result.file_path}')

        result = self.mode_logic(args, validation_result)
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

    def mode_logic(self, args, validation_result):
        if args.no_db:
            return validation_result, EXIT_CODE.SUCCESS, None

        print(f'SELF STORAGE: {self.storage}')

        storage = self.storage or PostgresStorage()
        db_result = storage.run(validation_result.valid_rows)

        if db_result.database_error:
            return validation_result, EXIT_CODE.DATABASE_ERROR, db_result

        return validation_result, EXIT_CODE.SUCCESS, db_result
