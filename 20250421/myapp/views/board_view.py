from flask import Blueprint

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/list/')
def list():
    return '게시판 목록'

@bp.route('/list/<id>/')
def view(id):
    return f'게시판 상세 페이지 {id}'
