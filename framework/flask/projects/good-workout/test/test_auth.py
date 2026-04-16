import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'nome_usuario': 'a', 'senha_usuario': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE nome_usuario = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('nome_usuario', 'senha_usuario', 'message'), (
    ('', '', b'nome_usuario is required.'),
    ('a', '', b'nome_usuario is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, nome_usuario, senha_usuario, message):
    response = client.post(
        '/auth/register',
        data={'nome_usuario': nome_usuario, 'senha_usuario': senha_usuario}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['nome_usuario'] == 'test'


@pytest.mark.parametrize(('nome_usuario', 'senha_usuario', 'message'), (
    ('a', 'test', b'Incorrect nome_usuario.'),
    ('test', 'a', b'Incorrect senha_usuario.'),
))
def test_login_validate_input(auth, nome_usuario, senha_usuario, message):
    response = auth.login(nome_usuario,senha_usuario )
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

