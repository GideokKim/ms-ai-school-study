import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from myapp.forms import ProfileForm
from myapp.models import User
from myapp.database import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if g.user is None:
        return redirect(url_for('auth.login'))
        
    form = ProfileForm()
    if form.validate_on_submit():
        # 현재 비밀번호 확인
        if not check_password_hash(g.user.password, form.current_password.data):
            flash('현재 비밀번호가 일치하지 않습니다.', 'error')
            return redirect(url_for('profile.profile'))
        
        # 프로필 이미지 처리
        if form.profile_image.data:
            # 프로필 이미지 디렉토리 생성
            profile_images_dir = os.path.join('static', 'profile_images')
            if not os.path.exists(profile_images_dir):
                os.makedirs(profile_images_dir)
                
            filename = secure_filename(form.profile_image.data.filename)
            filepath = os.path.join(profile_images_dir, filename)
            form.profile_image.data.save(filepath)
            g.user.profile_image = f'profile_images/{filename}'
        
        # 사용자 정보 업데이트
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.bio = form.bio.data
        
        # 새 비밀번호가 입력된 경우 업데이트
        if form.new_password.data:
            g.user.set_password(form.new_password.data)
        
        db.session.commit()
        flash('프로필이 성공적으로 업데이트되었습니다.', 'success')
        return redirect(url_for('profile.profile'))
    
    # GET 요청 시 현재 사용자 정보로 폼 초기화
    if request.method == 'GET':
        form.username.data = g.user.username
        form.email.data = g.user.email
        form.bio.data = g.user.bio
    
    return render_template('profile/profile.html', form=form) 