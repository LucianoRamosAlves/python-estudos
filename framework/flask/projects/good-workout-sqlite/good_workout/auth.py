import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from good_workout.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario', '').strip()
        password = request.form.get('senha', '').strip()

        db = get_db()
        error = None

        if not nome_usuario:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = db.execute(
                'SELECT id FROM usuario WHERE nome_usuario = ?',
                (nome_usuario,)
            ).fetchone()

            if user is not None:
                error = 'already registered'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO usuario (nome_usuario, senha_usuario) VALUES (?, ?)',
                    (nome_usuario, generate_password_hash(password))
                )
                db.commit()
            except Exception:
                error = 'already registered'
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario', '').strip()
        password = request.form.get('senha', '').strip()

        db = get_db()
        error = None

        if not nome_usuario:
            error = 'Nome de usuário é obrigatório.'
        elif not password:
            error = 'Senha é obrigatória.'
        else:
            user = db.execute(
                'SELECT * FROM usuario WHERE nome_usuario = ?',
                (nome_usuario,)
            ).fetchone()

            if user is None:
                error = 'Nome de usuário incorreto.'
            elif not check_password_hash(user['senha_usuario'], password):
                error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('private.dashboard'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM usuario WHERE id = ?',
            (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
