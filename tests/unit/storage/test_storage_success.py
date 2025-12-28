def test_storage_insert_success(storage):
    rows = [
        (1, 'artem', 1000),
        (2, 'john', 100)
    ]

    result  = storage.run(rows)

    assert result.database_error is None
    assert result.database_result['attempted'] == 2
    assert result.database_result['inserted'] == 2
    assert result.database_result['ignored'] == 0

def test_storage_ignore_duplicate(storage):
    rows = [
        (1, 'artem', 100),
        (1, 'artem', 100),
        (1, 'artem', 100)
    ]

    result = storage.run(rows)

    assert result.database_error is None
    assert result.database_result['attempted'] == 3
    assert result.database_result['inserted'] == 1
    assert result.database_result['ignored'] == 2

def test_storage_empty_rows(storage):
    rows = []

    result = storage.run(rows)

    assert result.database_error is None
    assert result.database_result['attempted'] == 0
    assert result.database_result['inserted'] == 0
    assert result.database_result['ignored'] == 0








