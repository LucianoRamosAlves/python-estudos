
#? aqui é como a recepção do hotel, onde os clientes chegam e se registram. aqui é onde os usuários podem criar uma conta, fazer login e sair da aplicação. aqui é onde a autenticação acontece, garantindo que apenas usuários autorizados possam acessar certas partes da aplicação.

import functools # de forma aimples, o módulo functools é importado para usar o decorador wraps, que é útil para criar decoradores personalizados que preservam as informações da função original.

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


from werkzeug.security import check_password_hash, generate_password_hash #* importo as funções check_password_hash e generate_password_hash do módulo werkzeug.security para lidar com a segurança das senhas dos usuários.

from flaskr.db import get_db #* importo a função get_db do módulo db para acessar o banco de dados e realizar operações relacionadas à autenticação dos usuários.


bp = Blueprint('auth', __name__, url_prefix='/auth') #* crio um blueprint para a autenticação, que é uma forma de organizar o código em partes reutilizáveis. o nome do blueprint é "auth" e o prefixo da URL é "/auth", o que significa que todas as rotas definidas neste blueprint terão "/auth" no início da URL.

#@ importo para o __init__.py


@bp.route('/register', methods=('GET', 'POST')) # defino uma rota para o registro de usuários, que aceita os métodos GET e POST. quando um usuário acessa esta rota com um método GET, ele verá um formulário de registro. quando ele envia o formulário com um método POST, os dados do formulário são processados para criar uma nova conta de usuário.
def register():
    if request.method == 'POST': #* verifico se o método da requisição é POST, o que significa que o formulário de registro foi enviado.
        nome_usuario = request.form['nome_usuario'] #* obtenho o nome de usuário do formulário.
        password = request.form['senha'] #* obtenho a senha do formulário.
        db = get_db() #* obtenho a conexão com o banco de dados usando a função get_db.
        cursor = db.cursor() #* crio um cursor para executar comandos SQL.
        error = None #* inicializo uma variável para armazenar mensagens de erro, se houver.

        if not nome_usuario: #* verifico se o nome de usuário não foi fornecido.
            error = 'Username is required.' #* se o nome de usuário não for fornecido, defino uma mensagem de erro.
        elif not password: #* verifico se a senha não foi fornecida.
            error = 'Password is required.' #* se a senha não for fornecida, defino uma mensagem de erro.
        else:
            cursor.execute( #* verifico se o nome de usuário já existe no banco de dados.
            'SELECT id FROM usuario WHERE nome_usuario = %s', (nome_usuario,)
        )
            user = cursor.fetchone() #* tento encontrar um usuário no banco de dados com o nome de usuário fornecido. se um usuário for encontrado, ele será armazenado na variável user. se nenhum usuário for encontrado, user será None.
        if user is not None:
            error = f"User {nome_usuario} is already registered." #* se o nome de usuário já existir, defino uma mensagem de erro.

        if error is None: #* se não houver erros, crio um novo usuário no banco de dados.
            try:
                cursor.execute(
                    'INSERT INTO usuario (nome_usuario, senha_usuario) VALUES (%s, %s)',
                    (nome_usuario, generate_password_hash(password)) #* insiro o nome de usuário e a senha hashada no banco de dados. a função generate_password_hash é usada para criar um hash seguro da senha antes de armazená-la no banco de dados.
                )
                db.commit() #* confirmo as alterações no banco de dados.
            except db.IntegrityError:
                error = f"User {nome_usuario} is already registered." #* se ocorrer um erro de integridade, defino uma mensagem de erro.
            else:
                return redirect(url_for('auth.login')) #* redireciono o usuário para a página de login após o registro bem-sucedido.

        flash(error) #* se houver um erro, uso a função flash para exibir a mensagem de erro para o usuário.

    return render_template('auth/register.html') #* se o método da requisição for GET ou se houver um erro, renderizo o template de registro para que o usuário possa tentar novamente ou ver os erros.

@bp.route('/login', methods=('GET', 'POST')) #* defino uma rota para o login de usuários, que aceita os métodos GET e POST. quando um usuário acessa esta rota com um método GET, ele verá um formulário de login. quando ele envia o formulário com um método POST, os dados do formulário são processados para autenticar o usuário.
def login():
    if request.method == 'POST': #* verifico se o método da requisição é POST, o que significa que o formulário de login foi enviado.
        nome_usuario = request.form['nome_usuario'] #* obtenho o nome de usuário do formulário.
        password = request.form['senha'] #* obtenho a senha do formulário.
        db = get_db() #* obtenho a conexão com o banco de dados usando a função get_db.
        cursor = db.cursor() #* crio um cursor para executar comandos SQL.
        error = None #* inicializo uma variável para armazenar mensagens de erro, se houver.
        cursor.execute( #* tento encontrar um usuário no banco de dados com o nome de usuário fornecido.
            'SELECT * FROM usuario WHERE nome_usuario = %s', (nome_usuario,)
        )
        user = cursor.fetchone() #* tento encontrar um usuário no banco de dados com o nome de usuário fornecido. se um usuário for encontrado, ele será armazenado na variável user. se nenhum usuário for encontrado, user será None.


        if user is None: #* se nenhum usuário for encontrado, defino uma mensagem de erro.
            error = 'Nome de usuário incorreto.'
        elif not check_password_hash(user['senha_usuario'], password): #* se a senha fornecida não corresponder à senha hashada armazenada no banco de dados, defino uma mensagem de erro. a função check_password_hash é usada para verificar se a senha fornecida corresponde ao hash armazenado no banco de dados.
            error = 'Senha incorreta.'

        if error is None: #* se não houver erros, autentico o usuário e inicio uma sessão para ele.
            session.clear() #* limpo a sessão atual para garantir que não haja dados antigos.
            session['user_id'] = user['id'] #* armazeno o ID do usuário na sessão para indicar que ele está autenticado.
            return redirect(url_for('private.dashboard')) #* redireciono o usuário para a página inicial após um login bem-sucedido.

        flash(error) #* se houver um erro, uso a função flash para exibir a mensagem de erro para o usuário.

    return render_template('auth/login.html') #* se o método da requisição for GET ou se houver um erro, renderizo o template de login para que o usuário possa tentar novamente ou ver os erros.

@bp.before_app_request #* defino uma função que será executada antes de cada requisição para carregar o usuário autenticado, se houver.
def load_logged_in_user():
    user_id = session.get('user_id') #* obtenho o ID do usuário da sessão, se estiver presente.

    if user_id is None: #* se não houver um ID de usuário na sessão, defino g.user como None.
        g.user = None
    else: #* se houver um ID de usuário na sessão, tento encontrar o usuário correspondente no banco de dados e armazená-lo em g.user para que possa ser acessado durante a requisição.
        db = get_db() #* obtenho a conexão com o banco de dados usando a função get_db.
        cursor = db.cursor() #* crio um cursor para executar comandos SQL.
        cursor.execute( #* tento encontrar o usuário correspondente ao ID armazenado na sessão.
            'SELECT * FROM usuario WHERE id = %s', (user_id,)
        )
        g.user = cursor.fetchone() #* armazeno o usuário encontrado em g.user para que possa ser acessado durante a requisição.
        
@bp.route('/logout') #* defino uma rota para o logout de usuários, que aceita apenas o método GET. quando um usuário acessa esta rota, ele será desconectado da aplicação.
def logout():
    session.clear() #* limpo a sessão para desconectar o usuário.
    return redirect(url_for('home')) #* redireciono o usuário para a página inicial após o logout.

def login_required(view): #* defino um decorador para proteger rotas que exigem autenticação. este decorador verifica se o usuário está autenticado antes de permitir o acesso à rota protegida.
    @functools.wraps(view) #* uso o decorador wraps para preservar as informações da função original, como seu nome e docstring.
    def wrapped_view(**kwargs): #* defino a função interna que será executada quando a rota protegida for acessada.
        if g.user is None: #* verifico se g.user é None, o que significa que o usuário não está autenticado.
            return redirect(url_for('auth.login')) #* se o usuário não estiver autenticado, redireciono-o para a página de login.

        return view(**kwargs) #* se o usuário estiver autenticado, chamo a função original da rota protegida com os argumentos fornecidos.

    return wrapped_view #* retorno a função interna como o resultado do decorador, permitindo que seja usada para proteger rotas que exigem autenticação.