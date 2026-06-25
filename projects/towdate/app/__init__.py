from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.public.routes import public
    app.register_blueprint(public)

    from app.private.routes import private
    app.register_blueprint(private)

    from app.auth.routes import auth
    app.register_blueprint(auth)

    return app