import sqlite3
from config import DB_PATH, TABLE_NAME


class Storage:
    def __init__(self):
        self.connect = sqlite3.connect(DB_PATH)
        self.cursor = self.connect.cursor()

    def create_or_open_database(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL
            )
        """)
        self.connect.commit()

    def data_save(self, valid_rows):
        attempted = len(valid_rows)
        before_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {TABLE_NAME}").fetchone()[0]
        try:
            with self.connect:
                self.cursor.executemany(
                    f'INSERT OR IGNORE INTO {TABLE_NAME} (id, name, salary) VALUES (?, ?, ?)',
                    valid_rows
                )
            after_insert = self.cursor.execute(f"SELECT COUNT(id) FROM {TABLE_NAME}").fetchone()[0]
            actual_insert = after_insert - before_insert
            ignored = attempted - actual_insert

            return {
                'database_result': {
                    'attempted': attempted,
                    'ignored': ignored,
                    'inserted': actual_insert
                }
            }

        except sqlite3.OperationalError as e:
            return {
                'database_error': {
                    'error': str(e)
                }
            }

    def close(self):
        self.connect.close()
