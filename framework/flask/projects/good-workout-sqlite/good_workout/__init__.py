import os
from flask import Flask, render_template, redirect, url_for


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'good_workout.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/')
    def home():
        return render_template('public/home/home.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import private
    app.register_blueprint(private.bp, url_prefix='/app')

    from . import blog
    app.register_blueprint(blog.bp, name='blog')

    return app
