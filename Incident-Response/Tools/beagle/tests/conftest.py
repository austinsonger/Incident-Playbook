import os
import pytest

from beagle.web import create_app
from beagle.web.server import db as _db
import tempfile

TESTDB = "test_project.db"
TESTDB_PATH = f"{tempfile.gettempdir()}/{TESTDB}"
TEST_DATABASE_URI = "sqlite:///" + TESTDB_PATH


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI}
    app = create_app()
    for k, v in settings_override.items():
        app.config[k] = v

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
