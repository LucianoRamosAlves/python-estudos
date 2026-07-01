from flask import session, redirect, url_for, flash, Flask, request
from flask_login import current_user, logout_user
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import Config
from app.extensions import db, migrate, login_manager, bcrypt


def create_app():

    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config.from_object(Config)
    bcrypt.init_app(app)  # Inicializa o Bcrypt com a instância do aplicativo
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.public.routes import public

    app.register_blueprint(public)

    from app.private.routes import private

    app.register_blueprint(private)

    from app.auth.routes import auth

    app.register_blueprint(auth)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(error):
        flash(
            "O arquivo enviado é muito grande. O limite permitido é de 5 MB.", "error"
        )
        if current_user.is_authenticated:
            return redirect(url_for("private.account"))
        return redirect(url_for("public.index"))

    @app.context_processor
    def inject_memory_fab_visibility():
        show_memory_fab = False

        if current_user.is_authenticated:
            endpoint = request.endpoint or ""
            show_memory_fab = not endpoint.startswith("private.account")

        return {"show_memory_fab": show_memory_fab}

    @app.before_request
    def check_session_version():
        if current_user.is_authenticated:
            if session.get("session_version") != current_user.session_version:
                logout_user()
                session.clear()
                flash("Sua sessão expirou. Por favor, faça login novamente.", "warning")
                return redirect(url_for("auth.login"))

    return app
