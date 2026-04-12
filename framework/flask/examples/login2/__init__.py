 
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'troque-essa-chave-por-uma-segura'


def validar_card(cartao):
    if not cartao:
        flash("O campo do cartão não pode ser vazio.", "card_error")
        return False

    cartao_str = str(cartao)

    if not cartao_str.isdigit():
        flash("O cartão deve conter apenas números.", "card_error")
        return False

    if len(cartao_str) != 7:
        flash("O cartão deve ter 7 dígitos.", "card_error")
        return False

    if cartao_str[3] != '0':
        flash("O quarto dígito deve ser 0.", "card_error")
        return False

    if cartao_str != "1230567":
        flash("Cartão incorreto.", "card_error")
        return False

    return True


def validar_pass(senha):
    if not senha:
        flash("Senha não pode ser vazia.", "senha_error")
        return False

    if not senha.isdigit():
        flash("A senha deve conter apenas números.", "senha_error")
        return False

    if len(senha) != 4:
        flash("A senha deve ter 4 dígitos.", "senha_error")
        return False

    if senha != "1234":
        flash("Senha incorreta.", "senha_error")
        return False

    return True


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('saldo'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        card = request.form['number_card']
        password = request.form['password']

        card_ok = validar_card(card)
        pass_ok = validar_pass(password)

        if card_ok and pass_ok:
            flash('Login bem-sucedido!', 'login_success')
            session['user'] = card
            return redirect(url_for('saldo'))
        else:
            flash('login falhou!', 'login_error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/erro')
def erro():
    return render_template('erro.html')

@app.route('/saldo')
def saldo():
    if 'user' not in session:
        flash('Faça login!', 'login_error')
        return redirect(url_for('erro'))

    user_card = session['user']
    saldo = 1000
    conta = f"{user_card[:3]}-0-{user_card[4:]}"
    return render_template('saldo.html', saldo=saldo, conta=conta, user_card=user_card)


@app.route('/contatos')
def contatos():
    return render_template('contatos.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)