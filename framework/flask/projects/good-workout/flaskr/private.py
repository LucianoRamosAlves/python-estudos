from flask import Blueprint, g, redirect, url_for, render_template
from flaskr.auth import login_required

bp = Blueprint('private', __name__, url_prefix='/app')

@bp.before_request #tudo depois precisa de login
@login_required
def require_login():
    if g.user is None:
        return redirect(url_for('auth.login'))

 
@bp.route('/dashboard')
def dashboard():
    return render_template('private/home/home.html') #* defino a rota para a página inicial da aplicação, que renderiza um template HTML localizado em templates/res/home.html.

@bp.route('/status')   
def status():
    return render_template('private/status/status.html')

@bp.route('/progresso')   
def progresso():
    return render_template('private/progresso/progresso.html')

@bp.route('/posts')   
def posts():
    return render_template('private/posts/posts.html')

@bp.route('/contato')   
def contato():
    return render_template('private/contato/contato.html')
    
@bp.route('/treinos')   
def treinos():
    return render_template('private/treinos/treinos.html')

        
@bp.route('/avisos')   
def avisos():
    return render_template('private/avisos/avisos.html')
