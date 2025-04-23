import config
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from .database import db, migrate
from .views import main_view, auth_view, question_view, answer_view, profile_view
from myapp import models

# .flaskenv 파일 로드
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login 설정
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(question_view.bp)
    app.register_blueprint(answer_view.bp)
    app.register_blueprint(profile_view.profile_bp)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_handler = RotatingFileHandler('logs/myapp.log', maxBytes=1024*1024*5, backupCount=5)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    return app
