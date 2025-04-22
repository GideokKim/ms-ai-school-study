import config
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from dotenv import load_dotenv
from .database import db, migrate
from .views import main_view, auth_view, board_view, sql_view
from myapp import models

# .flaskenv 파일 로드
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(board_view.bp)
    # app.register_blueprint(sql_view.bp)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_handler = RotatingFileHandler('logs/myapp.log', maxBytes=1024*1024*5, backupCount=5)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    return app
