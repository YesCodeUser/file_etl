import sqlite3

def test_storage_connection_error(storage, monkeypatch):
    def connection_error(db_path):
        raise sqlite3.Error

    monkeypatch.setattr('sqlite3.connect', connection_error)

    result = storage.run([(1, 'artem', 100)])

    assert result.database_error is not None
    assert isinstance(result.database_error, sqlite3.Error)


def test_storage_wrong_table_name(storage, monkeypatch):
    monkeypatch.setattr('config.TABLE_NAME', 'bad_name')
    row = [(1, 'artem', 100)]

    result = storage.run(row)

    assert result.database_error is not None
    assert isinstance(result.database_error, ValueError)


def test_storage_validate_schema_error(storage, monkeypatch):
    from storage.sqlite import Storage
    def falling_validate_schema(self):
        raise sqlite3.DatabaseError

    monkeypatch.setattr(Storage, 'validate_schema', falling_validate_schema)
    result = storage.run([(1, 'artem', 100)])

    assert result.database_error is not None
    assert isinstance(result.database_error, sqlite3.DatabaseError)


def test_storage_transaction_failed(storage, monkeypatch):
    from storage.sqlite import Storage
    def transaction_failed(self, valid_rows):
        raise sqlite3.Error

    monkeypatch.setattr(Storage, 'data_save', transaction_failed)

    result = storage.run([(1, 'artem', 100)])

    assert result.database_error is not None
    assert isinstance(result.database_error, sqlite3.Error)


