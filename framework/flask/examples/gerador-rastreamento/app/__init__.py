from flask import Flask
from app.routes import register_routes
from app.extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rastreamento.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_routes(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
