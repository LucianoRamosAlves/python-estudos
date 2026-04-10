from flask import Flask

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    #| aqui eu posso pegar os dados do formulário de login usando request.form, e depois usar o logger para registrar um evento de login
    username = request.form.get['username']
    password = request.form.post['password']
    
    #| aqui eu posso verificar se o username e password são válidos, e se forem, eu posso usar o logger para registrar um evento de login bem-sucedido
    if not username or not password:
        app.logger.error('Login falhou: username ou password ausente')
        return 'Login falhou!', 400
    if username != 'admin' or password != '1234':
        #| aqui eu posso usar o logger para registrar um evento de login falho, e também para registrar uma tentativa de ataque de força bruta, caso haja muitas tentativas falhas
        app.logger.warning(f'Tentativa de login falha para o usuário {username}')
        return 'Login falhou!'
    
    app.logger.info(f'Usuário {username} login bem-sucedido')
    return 'bem vindo!'
