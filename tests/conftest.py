import pytest
import psycopg
import config
from core.application import Application
from config import REQUIREMENTS_HEADERS
from storage.postgres import PostgresStorage


@pytest.fixture
def pg_conn():
    conn = psycopg.connect(config.get_database_url())
    conn.autocommit = False
    yield conn
    conn.rollback()
    conn.close()


@pytest.fixture
def storage(pg_conn):
    return PostgresStorage(conn=pg_conn)


@pytest.fixture
def application(file_csv, storage):
    return Application(
        str(file_csv),
        storage=storage,
        requirements_headers=REQUIREMENTS_HEADERS
    )


@pytest.fixture
def application_no_db(file_csv):
    return Application(
        str(file_csv),
        storage=None,
        requirements_headers=REQUIREMENTS_HEADERS
    )


@pytest.fixture
def file_txt(tmp_path):
    file = tmp_path / 'data.txt'
    return file


@pytest.fixture
def file_csv(tmp_path):
    file = tmp_path / 'data.csv'
    return file


@pytest.fixture
def mock_args(file_csv):
    class MockArgs:
        def __init__(self):
            self.file_path = str(file_csv)
            self.no_db = False
            self.json = False

    return MockArgs()
