import pytest
from storage.sqlite import Storage


@pytest.fixture
def storage(tmp_path):
    db_path = tmp_path / 'data.db'
    return Storage(db_path)


@pytest.fixture
def file(tmp_path):
    file = tmp_path / 'data.csv'
    return file
