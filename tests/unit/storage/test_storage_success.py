from storage.postgres import PostgresStorage


def test_storage_insert_success(pg_conn):
    valid_rows = [
        (30, 'artem', 100),
        (31, 'john', 200)
    ]

    storage = PostgresStorage(conn=pg_conn)
    result = storage.run(valid_rows)

    assert result.database_error is None
    assert result.database_result["attempted"] == 2
    assert result.database_result["inserted"] == 2
    assert result.database_result["ignored"] == 0


def test_storage_ignore_duplicate(pg_conn):
    valid_rows = [
        (30, 'artem', 200),
        (30, 'artem', 200),
        (30, 'artem', 200)
    ]

    storage = PostgresStorage(conn=pg_conn)
    result = storage.run(valid_rows)

    assert result.database_error is None
    assert result.database_result['attempted'] == 3
    assert result.database_result['inserted'] == 1
    assert result.database_result['ignored'] == 2


def test_storage_empty_rows(pg_conn):
    valid_rows = []

    storage = PostgresStorage(conn=pg_conn)
    result = storage.run(valid_rows)

    assert result.database_error is None
    assert result.database_result['attempted'] == 0
    assert result.database_result['inserted'] == 0
    assert result.database_result['ignored'] == 0
