import os
from flask import Flask
import pymysql # pois irei usar o MySQL como banco de dados, preciso importar a biblioteca pymysql para conectar o Flask ao MySQL.
from flask import current_app, g #* importo current_app e g do Flask para usar a aplicação atual e armazenar a conexão com o banco de dados.

def create_app(test_config=None): #* crio a fabrica de app, controi o app
    
    app = Flask(__name__, instance_relative_config=True) #* __name__ é o nome do módulo atual, e instance_relative_config=True ativa uma pasta separada para coisas sensíveis, como o banco de dados.
    
    app.config.from_mapping( #* configuro a aplicação com algumas configurações padrão, como a chave secreta e o caminho do banco de dados.
        SECRET_KEY='dev',
        DB_HOST='localhost',
        DB_USER='root',
        DB_PASSWORD='B34tB0x@',
        DB_NAME='bom_treino',

    )
    
    def get_db(): #* defino uma função para conectar ao banco de dados MySQL usando as configurações fornecidas.
        if 'db' not in g: #* verifico se a conexão com o banco de dados já existe na variável g, que é um objeto global para armazenar dados durante a aplicação.
            g.db = pymysql.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_NAME'],
                cursorclass=pymysql.cursors.DictCursor
            )
        return g.db
    
    def close_db(e=None): #* defino uma função para fechar a conexão com o banco de dados quando a aplicação for encerrada.
        db = g.pop('db', None)
        if db is not None:
            db.close()

    app.teardown_appcontext(close_db) #* registro a função close_db para ser chamada automaticamente quando o contexto da aplicação for encerrado.

    if test_config is None: #* se não for fornecida uma configuração de teste, carrego a configuração do arquivo config.py, se existir.
        app.config.from_pyfile('config.py', silent=True)
    else: #* se for fornecida uma configuração de teste, uso essa configuração para configurar a aplicação.
        app.config.from_mapping(test_config)
        
    os.makedirs(app.instance_path, exist_ok=True) #* garanto que a pasta de instância exista, criando-a se necessário. crio o cofre se nõ tiver um, para guardar coisas sensíveis como o banco de dados.
        
    @app.route('/dbtest') 
    def db_test(): #* defino uma rota de teste para verificar se a conexão com o banco de dados está funcionando corretamente.
        try:
            connection = get_db() #* tento conectar ao banco de dados usando a função get_db.
            with connection.cursor() as cursor: #* se a conexão for bem-sucedida, crio um cursor para executar uma consulta simples.
                cursor.execute('SELECT 1') #* executo uma consulta SQL simples para testar a conexão.
                result = cursor.fetchone() #* obtenho o resultado da consulta.
                return f'Conexão bem-sucedida! Resultado da consulta: {result}' #* retorno uma mensagem indicando que a conexão foi bem-sucedida e mostro o resultado da consulta.
        except Exception as e: #* se ocorrer algum erro durante a conexão ou a consulta, capturo a exceção e retorno uma mensagem de erro.
            return f'Erro ao conectar ao banco de dados: {e}'
   
    return app
