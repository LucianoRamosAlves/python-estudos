from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("public/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    erros = {}

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        # Validação do e-mail
        if not email:
            erros["email"] = "Informe seu e-mail."

        elif "@" not in email or "." not in email:
            erros["email"] = "E-mail inválido."

        # Validação da senha
        if not senha:
            erros["senha"] = "Informe sua senha."

        elif len(senha) < 3:
            erros["senha"] = "A senha deve possuir pelo menos 3 caracteres."

        # Se não houver erros
        if not erros:

            # Futuramente:
            # consultar banco de dados
            # verificar senha
            # criar sessão

            return redirect(url_for("home"))

    return render_template(
        "auth/login.html",
        erros=erros
    )


@app.route("/cadastro")
def cadastro():
    return render_template("auth/cadastro.html")


if __name__ == "__main__":
    app.run(debug=True)  