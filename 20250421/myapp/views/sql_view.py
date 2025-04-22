from flask import Blueprint, abort
from myapp import db
from myapp.models import User, Question, Answer
from datetime import datetime

bp = Blueprint('sql', __name__, url_prefix='/sql')

@bp.route('/create_user/')
def create_user():
    user = User(username='testuser', password='1234', email='test@test.com')
    db.session.add(user)
    db.session.commit()
    return 'User created!'

@bp.route('/create/')
def create():
    user = User.query.filter_by(username='testuser').first()
    if user is None:
        abort(404, description='User not found')

    q = Question(subject='질문 제목', content='질문 내용', create_date=datetime.now(), user=user)
    db.session.add(q)
    db.session.commit()
    return f'Question({q.id}) created!'

@bp.route('/read/')
def read():
    questions = Question.query.all()
    result = ''
    for q in questions:
        result += f'Question({q.id}) {q.subject}<br>'
    return result

@bp.route('/update/')
def update():
    q = Question.query.get(1)
    if q is None:
        abort(404, description='Question not found')

    q.subject = '수정된 질문 제목'
    q.modify_date = datetime.now()
    db.session.commit()
    return f'Question({q.id}) updated!'

@bp.route('/delete/')
def delete():
    q = Question.query.get(1)
    if q is None:
        abort(404, description='Question not found')

    db.session.delete(q)
    db.session.commit()
    return f'Question({q.id}) deleted!'

@bp.route("/answer/create/")
def answer_create():
    user = User.query.filter_by(username="testuser").first()
    question = Question.query.first()
    if user is None or question is None:
        abort(404, description="해당 사용자 또는 질문을 찾을 수 없습니다.")
    a = Answer(
        content="답변입니다.", create_date=datetime.now(), question=question, user=user
    )
    db.session.add(a)
    db.session.commit()
    return f"{a.id}번 답변을 등록했습니다."