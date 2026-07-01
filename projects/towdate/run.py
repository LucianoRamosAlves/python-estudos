from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    #TODO: LEMBRAR de remover debug=True em produção e configurar o servidor web (como Gunicorn ou uWSGI) para servir a aplicação Flask.
    