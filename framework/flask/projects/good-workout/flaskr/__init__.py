import os
from flask import Flask

def create_app(test_config=None): #* crio a fabrica de app, controi o app
    
    app = Flask(__name__, instance_relative_config=True) #* __name__ é o nome do módulo atual, e instance_relative_config=True ativa uma pasta separada para coisas sensíveis, como o banco de dados.
    
    app.config.from_mapping( #* configuro a aplicação com algumas configurações padrão, como a chave secreta e o caminho do banco de dados.
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    

    if test_config is None: #* se não for fornecida uma configuração de teste, carrego a configuração do arquivo config.py, se existir.
        app.config.from_pyfile('config.py', silent=True)
    else: #* caso contrário, uso a configuração de teste fornecida.
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) #* tento criar o diretório de instância, onde o banco de dados será armazenado. Se ele já existir, ignoro o erro.
    except OSError:
        pass

    from . import db
    db.init_app(app) #* importo o módulo db e inicializo a aplicação com ele.

    from . import auth
    app.register_blueprint(auth.bp) #* importo o módulo auth e registro seu blueprint na aplicação.

    from . import blog
    app.register_blueprint(blog.bp) #* importo o módulo blog e registro seu blueprint na aplicação.

    app.add_url_rule('/', endpoint='index') #* adiciono uma regra de URL para a raiz do site, associando-a ao endpoint 'index'.

    return app