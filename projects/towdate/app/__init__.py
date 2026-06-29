from flask import session, redirect, url_for, flash
from flask_login import current_user, logout_user
from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager, bcrypt

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )


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

    @app.before_request
    def check_session_version():
        if current_user.is_authenticated:
            if session.get("session_version") != current_user.session_version:
                logout_user()
                session.clear()
                flash(
                    "Sua sessão expirou. Por favor, faça login novamente.",
                    "warning"
                )
                return redirect(url_for("auth.login"))
    return app