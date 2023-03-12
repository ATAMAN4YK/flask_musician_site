import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import configs

bootstrap = Bootstrap5()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.autorization'


def crete_app(config_name):
    app = Flask(__name__, template_folder='./templates')
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
