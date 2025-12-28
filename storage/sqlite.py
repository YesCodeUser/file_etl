import logging
import sqlite3

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
            self.data_save(valid_rows)

        except(sqlite3.Error, ValueError) as e:
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
        if not Storage.is_valid_table_name():
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

    def data_save(self, valid_rows):
        attempted = len(valid_rows)
        before_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {config.TABLE_NAME}").fetchone()[0]
        try:
            with self.connection:
                self.cursor.executemany(
                    f'INSERT OR IGNORE INTO {config.TABLE_NAME} (id, name, salary) VALUES (?, ?, ?)',
                    valid_rows
                )
            after_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {config.TABLE_NAME}").fetchone()[0]
            actual_insert = after_insert - before_insert
            ignored = attempted - actual_insert

            logger.info('Adding rows to the database was successful.')
            self.result.database_result = {
                'attempted': attempted,
                'ignored': ignored,
                'inserted': actual_insert
            }

        except sqlite3.Error as e:
            logger.error(f'Transaction failed: {e}')
            raise

    def safe_close(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.cursor = None
                logger.debug('Database connection closed')
            except sqlite3.Error as e:
                logger.warning(f'Error while close connection {e}')

    @staticmethod
    def is_valid_table_name():
        return config.TABLE_NAME in config.ALLOWED_TABLES_NAME
