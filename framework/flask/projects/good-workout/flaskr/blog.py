from flask import (
    Blueprint, flash, g, redirect, render_template, request,  url_for
)

from werkzeug.exceptions import abort  
from flaskr.auth import login_required
from flaskr.db import get_db #* importo a função get_db do módulo db para acessar o banco de dados e realizar operações relacionadas à autenticação dos usuários.

bp = Blueprint('blog', __name__, url_prefix='/posts')#* crio um blueprint para a autenticação, que é uma forma de organizar o código em partes reutilizáveis. o nome do blueprint é "auth" e o prefixo da URL é "/auth", o que significa que todas as rotas definidas neste blueprint terão "/auth" no início da URL.

@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    SELECT p.id, p.title, p.descricao, p.created_at,
           p.author_id, p.image_url, u.nome_usuario AS usuario
    FROM posts p
    LEFT JOIN usuario u ON p.author_id = u.id
    ORDER BY p.created_at DESC
    """)

    posts = cursor.fetchall()

    return render_template('private/posts/posts.html', posts=posts)
    
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        descricao = request.form['descricao']
        image_url = request.form['image_url']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                'INSERT INTO posts (title, descricao, image_url, author_id) '
                'VALUES (%s, %s, %s, %s)',
                (title, descricao, image_url, g.user['id'])
            )

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('private/create/create.html')

def get_post(id, check_author=True):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'SELECT p.id, p.title, p.descricao, p.created_at, '
        'p.author_id,  p.image_url, u.nome_usuario AS usuario '
        'FROM posts p JOIN usuario u ON p.author_id = u.id '
        'WHERE p.id = %s',
        (id,)
    )

    post = cursor.fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)

    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    db.commit()

    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        descricao = request.form['descricao']
        image_url = request.form['image_url']
        error = None

        if not title:
            error = 'Título é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                'UPDATE posts SET title = %s, descricao = %s, image_url = %s '
                'WHERE id = %s',
                (title, descricao, image_url, id)
            )

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('private/update/update.html', post=post)



