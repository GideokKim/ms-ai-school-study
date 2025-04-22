import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# WAL 모드와 타임아웃 설정 추가
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "myproject.db")}?timeout=30&mode=rwc&journal_mode=WAL'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# 디버그 모드 활성화
DEBUG = True