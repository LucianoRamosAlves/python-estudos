Navegador
    ↓
run.py
    ↓
create_app()
    ↓
Blueprint
    ↓
Rota
    ↓
Função
    ↓
Template
    ↓
HTML
    ↓
Navegador


O run.py
Seu run.py é a porta de entrada.
Exemplo:
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
Quando você executa:
python run.py
o Python começa a executar esse arquivo.
2. O create_app()
Dentro de:
app/__init__.py
você tem algo parecido com:
from flask import Flask

def create_app():
    app = Flask(__name__)

    return app
Aqui você cria a aplicação Flask.
Pense assim:
Flask = motor do carro
create_app() = montar o carro
run.py = ligar o carro
3. Registrar Blueprints
Você criou:
app/
├── public/
├── auth/
└── private/
Cada pasta cuida de uma parte do sistema.
Por exemplo:
public  -> páginas públicas
auth    -> login e cadastro
private -> área logada
Dentro de public/routes.py:
from flask import Blueprint

public = Blueprint("public", __name__)
Aqui você cria um Blueprint.
O que é um Blueprint?
Imagine um shopping.
Cada loja é independente.
Shopping
├── Loja de roupas
├── Loja de sapatos
└── Loja de eletrônicos
O Flask é o shopping.
Os Blueprints são as lojas.
4. Registrar o Blueprint
No create_app():
from app.public.routes import public

app.register_blueprint(public)
Aqui você fala:
Flask, use também as rotas que estão dentro do Blueprint public.
Sem isso:
Flask
↓
não conhece a rota
↓
404 Not Found
Foi exatamente o erro que você teve.
5. A rota
Dentro de:
@public.route("/")
def home():
Você está dizendo:
URL "/"
↓
executa home()
Então quando alguém entra em:
http://127.0.0.1:5000/
o Flask chama:
home()
6. O template
Dentro da função:
return render_template("public/index.html")
O Flask procura:
app/templates/public/index.html
e devolve esse HTML para o navegador.