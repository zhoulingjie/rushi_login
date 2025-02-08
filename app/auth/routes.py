# rushi_login/app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, current_user
from app.models import User
from .forms import LoginForm, RegistrationForm  # 新增表单类
from . import bp  # 导入蓝图对象
from app.extensions import db, init_cache  # 导入 db 实例,Redis 初始化函数

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))

    form = LoginForm()
    redis_client = init_cache(current_app)  # 获取 Redis 客户端

    # 获取用户 IP 地址
    user_ip = request.remote_addr

    # 检查登录尝试次数
    login_attempts_key = f'login_attempts:{user_ip}'
    login_attempts = redis_client.get(login_attempts_key)

    if login_attempts is not None and int(login_attempts) >= 5:
        flash('登录失败次数过多，请 5 分钟后再试')
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            # 登录成功，清除登录尝试次数
            redis_client.delete(login_attempts_key)
            return redirect(url_for('auth.welcome'))
        else:
            # 登录失败，增加登录尝试次数
            redis_client.incr(login_attempts_key)
            # 设置过期时间为 5 分钟
            redis_client.expire(login_attempts_key, 300)
            flash('用户名或密码错误')

    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username and password:
            user = User(username=username)
            user.set_password(password)
            user.email = email
            db.session.add(user)
            db.session.commit()
            # return jsonify({"message": "User created"}), 201
            flash('成功注册用户')
            return redirect(url_for('auth.login'))
        else:
            flash('用户名或密码或邮箱缺失')
            form = RegistrationForm()
            return render_template('register.html', form=form)
            # return jsonify({"error": "用户名或密码或邮箱缺失"}), 400
    else:
        form = RegistrationForm()
        return render_template('register.html', form=form)

# 新增 logout 路由
@bp.route('/logout')
def logout():
    logout_user()
    flash('你已成功退出登录')
    return redirect(url_for('auth.login'))

@bp.route('/welcome')
def welcome():
    return render_template('welcome.html', username=current_user.username)