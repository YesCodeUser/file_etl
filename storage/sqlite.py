import logging
import sqlite3

import pandas as pd

import config
from core.storage_result import StorageResult

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.result = StorageResult()

    def run(self, valid_rows):
        try:
            self.connect()
            self.validate_schema()

            if not valid_rows:
                self.result.database_result = {
                    "attempted": 0,
                    "ignored": 0,
                    "inserted": 0,
                }
                return self.result

            df = self._rows_to_dataframe(valid_rows)
            self._save_dataframe(df)

        except Exception as e:
            logger.error(f'Database error: {e}')
            self.result.database_error = e
            return self.result

        finally:
            self.safe_close()

        return self.result

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logger.error(f'Cannot connect to database: {e}')
            raise

    def validate_schema(self):
        if not Storage._is_valid_table_name():
            raise ValueError(f'Table name "{config.TABLE_NAME}" is not allowed.'
                             f'Allowed names: {config.ALLOWED_TABLES_NAME}')

        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {config.TABLE_NAME}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                salary REAL NOT NULL
                )
            """)
            self.connection.commit()
        except sqlite3.DatabaseError as e:
            logger.error(f'Failed to create or open database: {e}')
            raise

    def _save_dataframe(self, df: pd.DataFrame):
        attempted = len(df)
        before_insert = self._count_rows()
        df = df.drop_duplicates(subset=['id'])

        try:
            df.to_sql(
                config.TABLE_NAME,
                self.connection,
                if_exists='append',
                index=False
            )

        except Exception as e:
            logger.error(f'DataFrame insert failed: {e}')
            self.result.database_result = {
                'attempted': attempted,
                'inserted': 0,
                'ignored': attempted
            }
            raise

        after_insert = self._count_rows()

        inserted = after_insert - before_insert
        ignored = attempted - inserted

        self.result.database_result = {
            "attempted": attempted,
            "inserted": inserted,
            "ignored": ignored,
        }

        logger.info(
            f"Database insert finished."
            f"Attempted={attempted}, Inserted={inserted}, Ignored={ignored}"
        )

    def safe_close(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.cursor = None
                logger.debug('Database connection closed')
            except Exception as e:
                logger.warning(f'Error while close connection {e}')

    @staticmethod
    def _is_valid_table_name():
        return config.TABLE_NAME in config.ALLOWED_TABLES_NAME

    @staticmethod
    def _rows_to_dataframe(valid_rows):
        df = pd.DataFrame(
            valid_rows,
            columns=['id', 'name', 'salary']
        )

        df['id'] = df['id'].astype(int)
        df['name'] = df['name'].astype(str)
        df['salary'] = df['salary'].astype(float)

        return df

    def _count_rows(self):
        return self.cursor.execute(
            f"SELECT COUNT(id) FROM {config.TABLE_NAME}"
        ).fetchone()[0]
