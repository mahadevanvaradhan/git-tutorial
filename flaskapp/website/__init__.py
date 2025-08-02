from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "mydb"

SECRET_KEY = os.getenv('SECRET_KEY', 'hjshjhdjahkjshkjdhjs')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://app_user:app_password@localhost:5438/mydb')




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .dashboard import dboard

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(dboard, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
