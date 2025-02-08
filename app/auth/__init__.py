# rushi_login/app/auth/__init__.py
from flask import Blueprint

# 创建蓝图对象
bp = Blueprint('auth', __name__)

# 导入视图模块，确保视图函数被注册到蓝图上
from . import routes