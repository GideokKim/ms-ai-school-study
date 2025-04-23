from flask import Blueprint, render_template, current_app, url_for
from myapp.models import Question
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # questions = Question.query.order_by(Question.create_date.desc())
    current_app.logger.info(f"main 페이지 접근")
    # return render_template('question/question_list.html', question_list=questions)
    return redirect(url_for('question.qlist'))

# @bp.route('/detail/<int:question_id>/')
# def detail(question_id):
#     question = Question.query.get(question_id)
#     current_app.logger.info(f"detail 페이지 접근")
#     return render_template('question/question_detail.html', question=question)