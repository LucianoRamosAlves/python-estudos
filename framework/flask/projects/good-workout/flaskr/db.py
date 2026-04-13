from flask import current_app, g #* importo current_app e g do Flask para usar a aplicação atual e armazenar a conexão com o banco de dados.
import pymysql # pois irei usar o MySQL como banco de dados, preciso importar a biblioteca pymysql para conectar o Flask ao MySQL.
import click #* importo click para criar comandos de linha de comando personalizados.

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
        
                
def init_db(): #* defino uma função para inicializar o banco de dados, criando as tabelas necessárias.
    db = get_db() #* obtenho a conexão com o banco de dados usando a função get_db.
    cursor = db.cursor() #* crio um cursor para executar comandos SQL.
        
    with current_app.open_resource('schema.sql') as f: #* abro o arquivo schema.sql, que contém os comandos SQL para criar as tabelas do banco de dados.
        sql = f.read().decode('utf-8') #* leio o conteúdo do arquivo e decodifico para uma string.
            
        commands = sql.split(';') #* divido os comandos SQL em partes usando o ponto e vírgula como separador.
            
        for command in commands: #* itero sobre cada comando SQL.
            if command.strip(): #* verifico se o comando não está vazio.
                cursor.execute(command) #* executo o comando SQL.


    db.commit() #* confirmo as alterações no banco de dados.
    cursor.close() #* fecho o cursor.

@click.command('init-db') #* defino um comando de linha de comando chamado "init-db" para inicializar o banco de dados usando a função init_db.   
def init_db_command(): #* defino um comando de linha de comando para inicializar o banco de dados usando a função init_db.
    """Clear the existing data and create new tables.""" #* descrição do comando.
    init_db() #* chamo a função init_db para inicializar o banco de dados.
    click.echo('Initialized the database.') #* imprimo uma mensagem indicando que o banco de dados foi inicializado.
    
def init_app(app): #* defino uma função para registrar as funções de banco de dados na aplicação Flask para que possam ser usadas em outros lugares da aplicação.
    app.teardown_appcontext(close_db) #* registro a função close_db para ser chamada automaticamente quando o contexto da aplicação for encerrado.
    app.cli.add_command(init_db_command) #* registro a função init_db_command como um comando de linha de comando para inicializar o banco de dados usando o comando "flask init-db". comando personalizado para inicializar o banco de dados usando o comando "flask init-db".
