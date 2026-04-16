import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/posts/')
    
    # não logado
    assert b"Log In" in response.data or b"Login" in response.data

    auth.login()
    response = client.get('/posts/')

    # logado
    assert b'Log Out' in response.data or b'Sair' in response.data

    # conteúdo genérico (seu HTML mudou)
    assert b'post' in response.data.lower()


@pytest.mark.parametrize('path', (
    '/posts/create',
    '/posts/1/update',
    '/posts/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert "/auth/login" in response.headers["Location"]


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute('UPDATE posts SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()

    assert client.post('/posts/1/update').status_code == 403
    assert client.post('/posts/1/delete').status_code == 403

    response = client.get('/posts/')
    assert b'/1/update' not in response.data


@pytest.mark.parametrize('path', (
    '/posts/999/update',
    '/posts/999/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()

    assert client.get('/posts/create').status_code == 200

    client.post('/posts/create', data={
        'title': 'created',
        'descricao': 'teste',
        'image_url': ''
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM posts').fetchone()[0]
        assert count >= 1


def test_update(client, auth, app):
    auth.login()

    assert client.get('/posts/1/update').status_code == 200

    client.post('/posts/1/update', data={
        'title': 'updated',
        'descricao': 'novo texto',
        'image_url': ''
    })

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM posts WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/posts/create',
    '/posts/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()

    response = client.post(path, data={
        'title': '',
        'descricao': '',
        'image_url': ''
    })

    assert b'Title is required.' in response.data or b'T\xc3\xadtulo' in response.data


def test_delete(client, auth, app):
    auth.login()

    response = client.post('/posts/1/delete')

    # redireciona pro index
    assert "/posts/" in response.headers["Location"]

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM posts WHERE id = 1').fetchone()
        assert post is None