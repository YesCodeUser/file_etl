import sqlite3


class Storage:
    def __init__(self):
        self.connect = sqlite3.connect('employees.db')
        self.cursor = self.connect.cursor()


    def create_or_open_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL
            )
        """)
        self.connect.commit()

    def data_save(self, valid_rows):
        attempted = len(valid_rows)
        before_insert = self.cursor.execute("SELECT COUNT(id) FROM employees").fetchone()[0]
        try:
            with self.connect:
                self.cursor.executemany(
                    'INSERT OR IGNORE INTO employees (id, name, salary) VALUES (?, ?, ?)',
                    valid_rows
            )
            after_insert = self.cursor.execute("SELECT COUNT(id) FROM employees").fetchone()[0]
            actual_insert = after_insert - before_insert
            ignored = attempted - actual_insert
            return {'attempted': attempted, 'ignored': ignored, 'inserted': actual_insert}
        except sqlite3.OperationalError as e:
            return {'error': str(e)}

    def close(self):
        self.connect.close()





