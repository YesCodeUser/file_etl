import logging
import sqlite3

from config import TABLE_NAME, ALLOWED_TABLES_NAME
from core.storage_result import StorageResult

logger = logging.getLogger(__name__)

#HACK Class Storage is doing too much, responsibility needs to separate
class Storage:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.result = StorageResult()

    def run(self, valid_rows):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logger.error(f'Cannot connect to database: {e}')
            self.result.database_error = f'Cannot connect to database: {e}'
            return self.result

        if not self._is_valid_table_name():
            logger.error(f'Table name "{TABLE_NAME}" is not allowed. '
                         f'Allowed names: {ALLOWED_TABLES_NAME}')
            self.result.database_error = (f'Table name "{TABLE_NAME}" is not allowed. '
                                          f'Allowed names: {ALLOWED_TABLES_NAME}')
            self.safe_close()
            return self.result

        try:
            self.create_or_open_database()
            self.data_save(valid_rows)
        except sqlite3.Error as e:
            self.result.database_error = e
            return self.result

        finally:
            self.safe_close()

        return self.result

    @staticmethod
    def _is_valid_table_name():
        return TABLE_NAME in ALLOWED_TABLES_NAME

    def create_or_open_database(self):
        try:
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                salary REAL NOT NULL
                )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f'Failed to create database: {e}')
            raise

    def data_save(self, valid_rows):
        attempted = len(valid_rows)
        before_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {TABLE_NAME}").fetchone()[0]
        try:
            with self.connection:
                self.cursor.executemany(
                    f'INSERT OR IGNORE INTO {TABLE_NAME} (id, name, salary) VALUES (?, ?, ?)',
                    valid_rows
                )
            after_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {TABLE_NAME}").fetchone()[0]
            actual_insert = after_insert - before_insert
            ignored = attempted - actual_insert

            logger.info('Adding rows to the database was successful.')
            self.result.database_result = {
                'attempted': attempted,
                'ignored': ignored,
                'inserted': actual_insert
            }

        except sqlite3.Error as e:
            logger.error(f'Database error: {e}')
            raise

    def safe_close(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.cursor = None
                logger.debug('Database connection closed')
            except Exception as e:
                logger.warning(f'Error while close connection {e}')

    #TODO separate method for test - add_connect()