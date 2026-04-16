import os
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db
from werkzeug.security import generate_password_hash  # 🔥 IMPORTANTE


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DB_HOST': 'localhost',
        'DB_USER': 'testuser',
        'DB_PASSWORD': '123456',
        'DB_NAME': 'flaskr_test',
    })

    with app.app_context():
        init_db()

        db = get_db()
        cursor = db.cursor()

        # limpa dados antes dos testes
        cursor.execute("DELETE FROM posts")
        cursor.execute("DELETE FROM usuario")

        # 🔥 CORREÇÃO PRINCIPAL AQUI (senha com hash)
        cursor.execute(
            "INSERT INTO usuario (nome_usuario, senha_usuario) VALUES (%s, %s)",
            ('test', generate_password_hash('test'))
        )

        cursor.execute(
            "INSERT INTO usuario (nome_usuario, senha_usuario) VALUES (%s, %s)",
            ('other2', generate_password_hash('test'))
        )

        # 🔥 ADICIONA ISSO
        cursor.execute(
            "INSERT INTO posts (title, descricao, image_url, author_id) VALUES (%s, %s, %s, %s)",
            ('test title', 'test\nbody', '', 1)
        )
        db.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, nome_usuario='test', senha_usuario='test'):
        return self._client.post(
            '/auth/login',
            data={
                'nome_usuario': nome_usuario,
                'senha': senha_usuario
            }
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)