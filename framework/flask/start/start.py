from flask import Flask
from flask import request #| isso serve para pegar os dados enviados pelo cliente, como formulários ou JSON
from markupsafe import escape #| isso serve para escapar caracteres especiais em strings, para evitar ataques de injeção de código
from flask import Flask, url_for #| isso serve para gerar URLs para as rotas da aplicação, baseado no nome da função que define a rota

app = Flask(__name__)

@app.route('/')
def hellow():
    return "<h1>Hello, World!</h1>"


#| uma aplicabilidade disso é criar uma rota que recebe um nome de usuário e retorna um perfil personalizado para esse usuário. Por exemplo, se o usuário acessar a rota /user/João, a aplicação pode retornar "Perfil, de João!".
@app.route('/user/<userName>')
def perfil(userName):
    return f"Perfil, de {escape(userName)}!"

#| nesse caso eu posso fazer um html para caada produto, e quando o usuário acessar a rota /produtos/Produto1, a aplicação pode retornar um html com as informações do Produto1. E assim por diante para cada produto.
@app.route('/produtos/<produtoNome>')
def produto(produtoNome):
    return f"Produto: {escape(produtoNome)}"


@app.route('/')
def home():
    return f'<a href="{url_for("comida", comidaNome="comida1")}">comida1</a>'

@app.route('/comida/<comidaNome>')
def comida(comidaNome):
    return f"Comida: {escape(comidaNome)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)