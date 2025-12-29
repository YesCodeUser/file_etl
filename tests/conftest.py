import pytest
from config import REQUIREMENTS_HEADERS
from storage.sqlite import Storage
from core.application import Application


@pytest.fixture
def storage(tmp_path):
    db_path = tmp_path / 'data.db'
    return Storage(db_path)


@pytest.fixture
def db_path(tmp_path):
    db_path = tmp_path / 'data.db'
    return db_path


@pytest.fixture
def file_txt(tmp_path):
    file = tmp_path / 'data.txt'
    return file


@pytest.fixture
def file_csv(tmp_path):
    file = tmp_path / 'data.csv'
    return file


@pytest.fixture
def application(file_csv, db_path):
    return Application(
        str(file_csv),
        REQUIREMENTS_HEADERS,
        db_path=db_path
    )


@pytest.fixture
def mock_args(file_csv):
    class MockArgs:
        def __init__(self):
            self.file_path = str(file_csv)
            self.no_db = False
            self.json = False

    return MockArgs()
