import logging
from pathlib import Path

import pandas as pd

from core.validation_result import ValidationResult

logger = logging.getLogger(__name__)


class Validation:
    def __init__(self, file_path, requirements_headers=None):
        self.file_path = Path(file_path)
        self.requirements_headers = requirements_headers or []
        self.result = ValidationResult(file_path)

    def run(self):
        logger.info(f'Start validation. File: {str(self.file_path)}')
        try:
            df = self._load_file()
            self._validate_structure(df)
        except(FileNotFoundError, IsADirectoryError, ValueError) as e:
            self.result.system_error = e
            return self.result

        self._validate_data(df)

        return self.result

    def _load_file(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f'File {self.file_path} does not exist')

        if not self.file_path.is_file():
            raise IsADirectoryError(f'File {self.file_path} is not a file')

        if self.file_path.suffix.lower() != '.csv':
            raise ValueError(f'File {self.file_path} is not .csv')

        df = pd.read_csv(
            self.file_path,
            dtype=str,
            keep_default_na=True
        )

        if df.empty:
            raise ValueError(f'File {self.file_path} is empty')

        return df

    def _validate_structure(self, df: pd.DataFrame):
        columns_lower = df.columns.str.lower()
        missing = set(self.requirements_headers) - set(columns_lower)

        if missing:
            raise ValueError(f'Missing columns: {",".join(missing)}')

        df.columns = columns_lower

    def _validate_data(self, df: pd.DataFrame):
        self.result.amount_rows = len(df)

        id_empty, id_not_int, id_less_zero, id_duplicate = Validation._validate_id(df)
        name_empty, name_invalid = Validation._validate_name(df)
        salary_empty, salary_not_float, salary_less_zero = Validation._validate_salary(df)

        invalid_mask = (
                id_empty | id_not_int | id_less_zero |
                id_duplicate | name_empty | name_invalid |
                salary_empty | salary_not_float | salary_less_zero
        )

        self._collect_errors(df, id_empty, 'id', 'id must not be empty')
        self._collect_errors(df, id_not_int, 'id', 'id must be integer')
        self._collect_errors(df, id_less_zero, 'id', 'id must be > 0')
        self._collect_errors(df, id_duplicate, 'id', 'duplicate id')

        self._collect_errors(df, name_empty, 'name', 'name must not be empty')
        self._collect_errors(df, name_invalid, 'name', 'invalid name')

        self._collect_errors(df, salary_empty, 'salary', 'salary must not be empty')
        self._collect_errors(df, salary_not_float, 'salary', 'salary must be float')
        self._collect_errors(df, salary_less_zero, 'salary', 'salary must be >= 0')

        valid_df = df.loc[~invalid_mask, ['id_int', 'name_str', 'salary_float']]

        for row in valid_df.itertuples(index=False):
            self.result.valid_rows.append((row.id_int, row.name_str, row.salary_float))

        self.result.amount_valid_rows = len(valid_df)
        self.result.amount_invalid_rows = self.result.amount_rows - self.result.amount_valid_rows

    @staticmethod
    def _validate_id(df: pd.DataFrame):
        df['id_int'] = pd.to_numeric(df['id'], errors="coerce")

        mask_id_empty = df['id'].isna() | df['id'].str.strip() == ''
        mask_id_not_int = df['id_int'].isna() & ~mask_id_empty
        mask_id_less_zero = df['id_int'] <= 0
        mask_id_duplicate = df['id_int'].duplicated(keep=False)

        return mask_id_empty, mask_id_not_int, mask_id_less_zero, mask_id_duplicate

    @staticmethod
    def _validate_name(df: pd.DataFrame):
        df['name_str'] = df['name'].astype(str)
        mask_name_empty = df['name'].isna() | (df['name_str'] == 'nan') | (df['name_str'].str.strip() == '')
        mask_valid_format = df['name_str'].str.match(r'^[A-Za-zА-Яа-яЁё\s\.]+$')

        mask_invalid_format = ~mask_valid_format & ~mask_name_empty

        return mask_name_empty, mask_invalid_format

    @staticmethod
    def _validate_salary(df: pd.DataFrame):
        df['salary_float'] = pd.to_numeric(df['salary'], errors='coerce')

        mask_salary_empty = df['salary'].isna() | df['salary'].str.strip() == ''
        mask_salary_not_float = df['salary_float'].isna()
        mask_salary_less_zero = df['salary_float'] < 0

        return mask_salary_empty, mask_salary_not_float, mask_salary_less_zero

    def _collect_errors(self, df: pd.DataFrame, mask, column, message):
        for idx in df[mask].index:
            self.result.errors.append({
                'line': idx + 2,
                'column': column,
                'message': message
            })
