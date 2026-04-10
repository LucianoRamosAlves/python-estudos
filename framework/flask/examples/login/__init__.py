from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey' #| isso é necessário para usar o flash, que é uma função do Flask que permite mostrar mensagens temporárias para o usuário, como erros ou sucessos. O secret_key é usado para criptografar as mensagens do flash, para garantir a segurança.

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #| aqui eu posso verificar se o username e password são válidos, e se forem, eu posso redirecionar o usuário para a página de perfil, usando url_for para gerar a URL da rota de perfil, e passando o nome do usuário como argumento.
        if username == 'admin' and password == '1234':
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('perfil', userName=username))
        else:
            flash('Login falhou! Verifique seu username e password.', 'danger')
    
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
