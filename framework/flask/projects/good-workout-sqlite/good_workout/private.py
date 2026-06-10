from flask import Blueprint, g, redirect, url_for, render_template, request, flash, jsonify
from good_workout.auth import login_required
from good_workout.db import get_db
from datetime import date

bp = Blueprint('private', __name__, url_prefix='/app')


@bp.before_request
@login_required
def require_login():
    if g.user is None:
        return redirect(url_for('auth.login'))


# ============================================================
# DASHBOARD
# ============================================================
@bp.route('/dashboard')
def dashboard():
    db = get_db()
    user_id = g.user['id']

    # Últimos progressos
    ultimo_progresso = db.execute(
        'SELECT * FROM progresso WHERE usuario_id = ? ORDER BY data_registro DESC LIMIT 1',
        (user_id,)
    ).fetchone()

    # Total de treinos
    total_treinos = db.execute(
        'SELECT COUNT(*) as total FROM treinos WHERE usuario_id = ?',
        (user_id,)
    ).fetchone()['total']

    # Total de posts
    total_posts = db.execute(
        'SELECT COUNT(*) as total FROM posts WHERE author_id = ?',
        (user_id,)
    ).fetchone()['total']

    # Mensagens não lidas
    msg_nao_lidas = db.execute(
        'SELECT COUNT(*) as total FROM contato_mensagens WHERE usuario_id = ? AND lida = 0',
        (user_id,)
    ).fetchone()['total']

    # Últimos treinos
    ultimos_treinos = db.execute(
        'SELECT * FROM treinos WHERE usuario_id = ? ORDER BY created_at DESC LIMIT 4',
        (user_id,)
    ).fetchall()

    return render_template('privado/home/home.html',
                         ultimo_progresso=ultimo_progresso,
                         total_treinos=total_treinos,
                         total_posts=total_posts,
                         msg_nao_lidas=msg_nao_lidas,
                         ultimos_treinos=ultimos_treinos)


# ============================================================
# TREINOS - CRUD Completo
# ============================================================
@bp.route('/treinos')
def treinos():
    db = get_db()
    user_id = g.user['id']

    treinos_lista = db.execute(
        'SELECT * FROM treinos WHERE usuario_id = ? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()

    return render_template('privado/treinos/treinos.html', treinos=treinos_lista)


@bp.route('/treinos/criar', methods=('GET', 'POST'))
def treino_criar():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        categoria = request.form.get('categoria', 'geral').strip()

        if not nome:
            flash('Nome do treino é obrigatório.', 'danger')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO treinos (nome_treino, descricao, categoria, usuario_id) VALUES (?, ?, ?, ?)',
                (nome, descricao, categoria, g.user['id'])
            )
            db.commit()
            flash('Treino criado com sucesso!', 'success')
            return redirect(url_for('private.treinos'))

    return render_template('privado/treinos/treino_form.html', treino=None)


@bp.route('/treinos/<int:id>/editar', methods=('GET', 'POST'))
def treino_editar(id):
    db = get_db()
    treino = db.execute(
        'SELECT * FROM treinos WHERE id = ? AND usuario_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if treino is None:
        flash('Treino não encontrado.', 'danger')
        return redirect(url_for('private.treinos'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        categoria = request.form.get('categoria', 'geral').strip()

        if not nome:
            flash('Nome do treino é obrigatório.', 'danger')
        else:
            db.execute(
                'UPDATE treinos SET nome_treino = ?, descricao = ?, categoria = ? WHERE id = ?',
                (nome, descricao, categoria, id)
            )
            db.commit()
            flash('Treino atualizado com sucesso!', 'success')
            return redirect(url_for('private.treinos'))

    return render_template('privado/treinos/treino_form.html', treino=treino)


@bp.route('/treinos/<int:id>/excluir', methods=('POST',))
def treino_excluir(id):
    db = get_db()
    db.execute('DELETE FROM treinos WHERE id = ? AND usuario_id = ?', (id, g.user['id']))
    db.commit()
    flash('Treino excluído com sucesso!', 'success')
    return redirect(url_for('private.treinos'))


@bp.route('/treinos/<int:id>')
def treino_detalhe(id):
    db = get_db()
    treino = db.execute(
        'SELECT * FROM treinos WHERE id = ? AND usuario_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if treino is None:
        flash('Treino não encontrado.', 'danger')
        return redirect(url_for('private.treinos'))

    exercicios = db.execute(
        'SELECT * FROM exercicios WHERE treino_id = ? ORDER BY ordem',
        (id,)
    ).fetchall()

    return render_template('privado/treinos/treino_detalhe.html', treino=treino, exercicios=exercicios)


# ============================================================
# EXERCÍCIOS (dentro de treinos)
# ============================================================
@bp.route('/treinos/<int:treino_id>/exercicio/criar', methods=('POST',))
def exercicio_criar(treino_id):
    nome = request.form.get('nome', '').strip()
    series = request.form.get('series', 3)
    repeticoes = request.form.get('repeticoes', '12')
    carga = request.form.get('carga', '').strip()
    observacao = request.form.get('observacao', '').strip()

    if not nome:
        flash('Nome do exercício é obrigatório.', 'danger')
    else:
        db = get_db()

        # Pega a próxima ordem
        max_ordem = db.execute(
            'SELECT COALESCE(MAX(ordem), 0) as max_ordem FROM exercicios WHERE treino_id = ?',
            (treino_id,)
        ).fetchone()['max_ordem']

        db.execute(
            'INSERT INTO exercicios (treino_id, nome, series, repeticoes, carga, observacao, ordem) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (treino_id, nome, series, repeticoes, carga, observacao, max_ordem + 1)
        )
        db.commit()
        flash('Exercício adicionado!', 'success')

    return redirect(url_for('private.treino_detalhe', id=treino_id))


@bp.route('/exercicio/<int:id>/excluir', methods=('POST',))
def exercicio_excluir(id):
    db = get_db()

    # Pega treino_id antes de excluir
    ex = db.execute('SELECT treino_id FROM exercicios WHERE id = ?', (id,)).fetchone()
    if ex:
        db.execute('DELETE FROM exercicios WHERE id = ?', (id,))
        db.commit()
        flash('Exercício removido.', 'success')
        return redirect(url_for('private.treino_detalhe', id=ex['treino_id']))

    flash('Exercício não encontrado.', 'danger')
    return redirect(url_for('private.treinos'))


# ============================================================
# PROGRESSO
# ============================================================
@bp.route('/progresso', methods=('GET', 'POST'))
def progresso():
    db = get_db()
    user_id = g.user['id']

    if request.method == 'POST':
        peso = request.form.get('peso', '').strip()
        altura = request.form.get('altura', '').strip()
        braco_esquerdo = request.form.get('braco_esquerdo', '').strip()
        braco_direito = request.form.get('braco_direito', '').strip()
        peito = request.form.get('peito', '').strip()
        cintura = request.form.get('cintura', '').strip()
        quadril = request.form.get('quadril', '').strip()
        coxa_esquerda = request.form.get('coxa_esquerda', '').strip()
        coxa_direita = request.form.get('coxa_direita', '').strip()
        observacao = request.form.get('observacao', '').strip()

        if not peso and not peito and not cintura:
            flash('Preencha pelo menos o peso ou alguma medida.', 'danger')
        else:
            db.execute("""
                INSERT INTO progresso
                (usuario_id, peso, altura, braco_esquerdo, braco_direito, peito, cintura, quadril, coxa_esquerda, coxa_direita, observacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id,
                  float(peso) if peso else None,
                  float(altura) if altura else None,
                  float(braco_esquerdo) if braco_esquerdo else None,
                  float(braco_direito) if braco_direito else None,
                  float(peito) if peito else None,
                  float(cintura) if cintura else None,
                  float(quadril) if quadril else None,
                  float(coxa_esquerda) if coxa_esquerda else None,
                  float(coxa_direita) if coxa_direita else None,
                  observacao))
            db.commit()
            flash('Progresso registrado com sucesso!', 'success')
            return redirect(url_for('private.progresso'))

    # Busca histórico
    historico = db.execute(
        'SELECT * FROM progresso WHERE usuario_id = ? ORDER BY data_registro DESC LIMIT 20',
        (user_id,)
    ).fetchall()

    return render_template('privado/progresso/progresso.html', historico=historico)


@bp.route('/progresso/<int:id>/excluir', methods=('POST',))
def progresso_excluir(id):
    db = get_db()
    db.execute('DELETE FROM progresso WHERE id = ? AND usuario_id = ?', (id, g.user['id']))
    db.commit()
    flash('Registro excluído.', 'success')
    return redirect(url_for('private.progresso'))


# ============================================================
# STATUS
# ============================================================
@bp.route('/status')
def status():
    db = get_db()
    user_id = g.user['id']

    # Último progresso
    ultimo = db.execute(
        'SELECT * FROM progresso WHERE usuario_id = ? ORDER BY data_registro DESC LIMIT 1',
        (user_id,)
    ).fetchone()

    # Penúltimo para comparar
    anterior = db.execute(
        'SELECT * FROM progresso WHERE usuario_id = ? ORDER BY data_registro DESC LIMIT 1 OFFSET 1',
        (user_id,)
    ).fetchone()

    # Total de treinos e exercícios
    stats = db.execute("""
        SELECT
            COUNT(DISTINCT t.id) as total_treinos,
            COUNT(e.id) as total_exercicios
        FROM treinos t
        LEFT JOIN exercicios e ON e.treino_id = t.id
        WHERE t.usuario_id = ?
    """, (user_id,)).fetchone()

    # Total de posts
    total_posts = db.execute(
        'SELECT COUNT(*) as total FROM posts WHERE author_id = ?',
        (user_id,)
    ).fetchone()['total']

    # Total de registros de progresso
    total_progresso = db.execute(
        'SELECT COUNT(*) as total FROM progresso WHERE usuario_id = ?',
        (user_id,)
    ).fetchone()['total']

    # Dias de academia (desde primeiro registro)
    primeiro = db.execute(
        'SELECT MIN(data_registro) as primeiro FROM progresso WHERE usuario_id = ?',
        (user_id,)
    ).fetchone()

    return render_template('privado/status/status.html',
                         ultimo=ultimo,
                         anterior=anterior,
                         stats=stats,
                         total_posts=total_posts,
                         total_progresso=total_progresso,
                         primeiro=primeiro)


# ============================================================
# CONTATO
# ============================================================
@bp.route('/contato', methods=('GET', 'POST'))
def contato():
    db = get_db()
    user_id = g.user['id']

    if request.method == 'POST':
        assunto = request.form.get('assunto', '').strip()
        mensagem = request.form.get('mensagem', '').strip()

        if not assunto or not mensagem:
            flash('Preencha todos os campos.', 'danger')
        else:
            db.execute(
                'INSERT INTO contato_mensagens (usuario_id, assunto, mensagem) VALUES (?, ?, ?)',
                (user_id, assunto, mensagem)
            )
            db.commit()
            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('private.dashboard'))

    # Busca mensagens do usuário
    mensagens = db.execute(
        'SELECT * FROM contato_mensagens WHERE usuario_id = ? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()

    return render_template('privado/contato/contato.html', mensagens=mensagens)


# ============================================================
# AVISOS
# ============================================================
@bp.route('/avisos')
def avisos():
    db = get_db()
    user_id = g.user['id']

    mensagens = db.execute(
        'SELECT * FROM contato_mensagens WHERE usuario_id = ? ORDER BY created_at DESC LIMIT 10',
        (user_id,)
    ).fetchall()

    return render_template('privado/avisos/avisos.html', mensagens=mensagens)


# ============================================================
# POSTS
# ============================================================
@bp.route('/posts')
def posts():
    return redirect(url_for('blog.index'))
