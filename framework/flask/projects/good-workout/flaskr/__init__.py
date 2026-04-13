import os
from flask import Flask

def create_app(test_config=None): #* crio a fabrica de app, controi o app
    
    app = Flask(__name__, instance_relative_config=True) #* __name__ é o nome do módulo atual, e instance_relative_config=True ativa uma pasta separada para coisas sensíveis, como o banco de dados.
    
    app.config.from_mapping( #* configuro a aplicação com algumas configurações padrão, como a chave secreta e o caminho do banco de dados.
        SECRET_KEY='dev',
        DB_HOST='localhost',
        DB_USER='root',
        DB_PASSWORD='B34tB0x@',
        DB_NAME='bom_treino',

    )
    if test_config is None: #* se não for fornecida uma configuração de teste, carrego a configuração do arquivo config.py, se existir.
        app.config.from_pyfile('config.py', silent=True)
    else: #* se for fornecida uma configuração de teste, uso essa configuração para configurar a aplicação.
        app.config.from_mapping(test_config)
        
    os.makedirs(app.instance_path, exist_ok=True) #* garanto que a pasta de instância exista, criando-a se necessário. crio o cofre se nõ tiver um, para guardar coisas sensíveis como o banco de dados.
    
    @app.route('/hello') #* defino uma rota de teste para verificar se a aplicação está funcionando corretamente.
    def hello():
        return 'Hello, World!'
    
    
    
    #| daqui para frente estao sendo encrementadas depois
    
    from . import db #* importo o módulo db para registrar as funções de banco de dados na aplicação.
    db.init_app(app) #* chamo a função init_app do módulo db para registrar as funções de banco de dados na aplicação.
    
    from . import auth #* importo o módulo auth para registrar as rotas de autenticação na aplicação.
    app.register_blueprint(auth.bp) #* registro o blueprint de autenticação na aplicação.
    

    return app

