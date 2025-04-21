from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html', title='기술 블로그', username='감자2')

@bp.route('/hello/')
def hello():
    return render_template('hello.html', repeat_count=10)