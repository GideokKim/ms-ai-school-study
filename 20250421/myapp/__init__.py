from flask import Flask
from dotenv import load_dotenv
from .views import main_view, auth_view, board_view

# .flaskenv 파일 로드
load_dotenv()

app = Flask(__name__)
app.register_blueprint(main_view.bp)
app.register_blueprint(auth_view.bp)
app.register_blueprint(board_view.bp)
