from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from good_workout.auth import login_required
from good_workout.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/posts')


@bp.route('/')
def index():
    db = get_db()

    posts = db.execute("""
        SELECT p.id, p.title, p.descricao, p.created_at,
               p.author_id, p.image_url, u.nome_usuario AS usuario
        FROM posts p
        LEFT JOIN usuario u ON p.author_id = u.id
        ORDER BY p.created_at DESC
    """).fetchall()

    return render_template('privado/posts/posts.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        descricao = request.form.get('descricao', '').strip()
        image_url = request.form.get('image_url', '').strip()
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            db.execute(
                'INSERT INTO posts (title, descricao, image_url, author_id) '
                'VALUES (?, ?, ?, ?)',
                (title, descricao, image_url, g.user['id'])
            )

            db.commit()

            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('privado/create/create.html')


def get_post(id, check_author=True):
    db = get_db()

    post = db.execute(
        'SELECT p.id, p.title, p.descricao, p.created_at, '
        'p.author_id, p.image_url, u.nome_usuario AS usuario '
        'FROM posts p JOIN usuario u ON p.author_id = u.id '
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

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
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    flash('Post deletado com sucesso!', 'danger')
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        descricao = request.form.get('descricao', '').strip()
        image_url = request.form.get('image_url', '').strip()
        error = None

        if not title:
            error = 'Título é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            db.execute(
                'UPDATE posts SET title = ?, descricao = ?, image_url = ? '
                'WHERE id = ?',
                (title, descricao, image_url, id)
            )

            db.commit()

            flash('Post atualizado com sucesso!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('privado/update/update.html', post=post)
