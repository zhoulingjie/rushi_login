# rushi_login/app/auth/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import User
from .forms import LoginForm, RegistrationForm  # 新增表单类
from . import bp  # 导入蓝图对象

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('auth.welcome'))
        flash('用户名或密码错误')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@bp.route('/welcome')
def welcome():
    return render_template('welcome.html', username=current_user.username)