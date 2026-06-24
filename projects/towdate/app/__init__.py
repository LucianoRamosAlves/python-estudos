from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    from app.public.routes import public
    app.register_blueprint(public)

    return app