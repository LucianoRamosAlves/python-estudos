import pytest
import pymysql
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # conexão deve estar fechada
    with pytest.raises(pymysql.err.Error):
        cursor = db.cursor()
        cursor.execute('SELECT 1')


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)

    result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called