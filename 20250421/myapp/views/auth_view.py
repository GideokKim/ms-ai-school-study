from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login/')
def login():
    return '아이디와 비번으로 로그인'

@bp.route('/signup/')
def signup():
    return '지금부터 회원가입을 진행합니다.'