from flask import Blueprint, render_template
from myapp.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    questions = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=questions)
