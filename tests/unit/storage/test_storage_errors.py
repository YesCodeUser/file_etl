from storage.postgres import PostgresStorage

def test_storage_connection_error(monkeypatch):
    import psycopg

    def connection_error(*args, **kwargs):
        raise psycopg.OperationalError("DB connection error")

    monkeypatch.setattr(psycopg, "connect", connection_error)

    storage = PostgresStorage()
    result = storage.run([(1, 'artem', 100)])

    assert result.database_error is not None

    print(f"DB ERROR: {result.database_error}")

    assert isinstance(result.database_error, psycopg.OperationalError)





