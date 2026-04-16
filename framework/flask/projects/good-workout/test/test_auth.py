import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register',
        data={
            'nome_usuario': 'a',
            'senha': 'a'
        }
    )

    assert "/auth/login" in response.headers["Location"]

    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM usuario WHERE nome_usuario = %s",
            ('a',)
        )
        user = cursor.fetchone()

        assert user is not None


@pytest.mark.parametrize(('nome_usuario', 'senha', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, nome_usuario, senha, message):
    response = client.post(
        '/auth/register',
        data={
            'nome_usuario': nome_usuario,
            'senha': senha
        }
    )

    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200

    response = auth.login()

    # agora é dashboard
    assert "/dashboard" in response.headers["Location"] or "/" in response.headers["Location"]

    with client:
        client.get('/')

        assert session.get('user_id') is not None
        assert g.user is not None
        assert g.user['nome_usuario'] == 'test'


@pytest.mark.parametrize(('nome_usuario', 'senha', 'message'), (
    ('a', 'test', b'Nome de usu\xc3\xa1rio incorreto.'),
    ('test', 'a', b'Senha incorreta.'),
))
def test_login_validate_input(auth, nome_usuario, senha, message):
    response = auth.login(nome_usuario, senha)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()

        assert 'user_id' not in session