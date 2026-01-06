import logging
from pathlib import Path

import psycopg

import config

from core.storage_result import StorageResult

logger = logging.getLogger(__name__)


class PostgresStorage:
    def __init__(self, conn=None):
        self.dsn = config.get_database_url()
        self.conn = conn
        self.owns_connection = conn is None
        self.result = StorageResult()

    def run(self, valid_rows):
        try:
            self._connect()
            self._begin()

            self._execute_sql_file("001_create_employees.sql")
            self._execute_sql_file("002_create_staging_employees.sql")
            self._execute_sql_file("003_truncate_staging.sql")

            self._load_to_staging(valid_rows)

            attempted, before = self._fetch_statistics()

            self._execute_sql_file("020_insert_employees.sql")
            _, after = self._fetch_statistics()

            inserted = after - before
            ignored = attempted - inserted

            self.result.database_result = {
                'attempted': attempted,
                'inserted': inserted,
                'ignored': ignored
            }

            self._commit()

        except Exception as e:
            logger.error(f"Database error: {e}")
            self._rollback()
            self.result.database_error = e

        finally:
            self._close()

        return self.result

    def _connect(self):
        if self.conn is None:
            self.conn = psycopg.connect(self.dsn)
            self.owns_connection = True
        logger.info("Connected to PostgreSQL")

    def _begin(self):
        if self.owns_connection:
            self.conn.cursor().execute("BEGIN;")

    def _commit(self):
        if self.owns_connection:
            self.conn.commit()
            logger.info("Transaction committed")

    def _rollback(self):
        if self.conn and self.owns_connection:
            self.conn.rollback()
            logger.warning("Transaction rolled back")

    def _close(self):
        if self.conn and self.owns_connection:
            self.conn.close()
            logger.info("Connection closed")

    def _execute_sql_file(self, file_name):
        sql_text = PostgresStorage._read_sql(file_name)
        with self.conn.cursor() as cur:
            # noinspection PyTypeChecker
            cur.execute(sql_text)


    def _fetch_statistics(self):
        sql_text = self._read_sql("030_count_statistics.sql")
        with self.conn.cursor() as cur:
            # noinspection PyTypeChecker
            cur.execute(sql_text)
            attempted, total = cur.fetchone()
        return attempted, total

    def _load_to_staging(self, valid_rows):
        sql_text = self._read_sql("010_insert_staging.sql.psycopg")

        with self.conn.cursor() as cur:
            # noinspection PyTypeChecker
            cur.executemany(sql_text, valid_rows)

    @staticmethod
    def _read_sql(file_name):
        base_path = Path(__file__).resolve().parent.parent / 'sql'

        for sql_file in base_path.rglob('*'):
            if sql_file.name == file_name:
                return sql_file.read_text(encoding='utf-8')

        raise FileNotFoundError(f'SQL file: {file_name} is not found')
