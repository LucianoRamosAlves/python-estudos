from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = 'secret_key' 

def validar_card(cartao):

    # 1. Não pode ser vazio
    if cartao is None or str(cartao).strip() == "":
        flash("O campo do cartão não pode ser vazio.", "card_error")
        return False

    # Converter para string
    cartao_str = str(cartao)

    # 2. Deve conter apenas números
    if not cartao_str.isdigit():
        flash("O campo do cartão deve conter apenas números.", "card_error")
        return False

    # 3. Deve ter exatamente 7 dígitos
    if len(cartao_str) != 7:
        flash("O campo do cartão deve ter exatamente 7 dígitos.", "card_error")
        return False

    # 4. O quarto dígito deve ser 0
    if cartao_str[3] != '0':
        flash("O quarto dígito deve ser 0 (ex: xxx0xxx).", "card_error")
        return False
    
    if cartao != "1230567":
        flash("Cartão incorreto. Tente novamente.", "card_error")
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
        flash("A senha deve ter exatamente 4 dígitos.", "senha_error")
        return False
    
    if senha != "1234":
        flash("Senha incorreta. Tente novamente.", "senha_error")
        return False
    
    return True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        number_card = request.form['number_card']
        password = request.form['password']
            
        card_ok = validar_card(number_card)
        pass_ok = validar_pass(password)

        if card_ok and pass_ok:
            return redirect(url_for('saldo'))
        
    return render_template('login.html')

@app.route('/saldo')
def saldo():
    # Lógica para obter o saldo aqui
    saldo = 1000  # Exemplo de saldo
    conta = "1234-5"  # Exemplo de número de conta
    return render_template('saldo.html', saldo=saldo, conta=conta)

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/logout')
def logout():
    # Lógica de logout aqui
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
