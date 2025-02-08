from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis
from urllib.parse import urlparse

db = SQLAlchemy()
login_manager = LoginManager()
cache = None  # 将在create_app中初始化

# 添加 user_loader 回调函数
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # 移动到函数内部
    # 根据用户 ID 从数据库中加载用户对象
    return User.query.get(int(user_id))

def init_cache(app):
    redis_url = urlparse(app.config['REDIS_URL'])
    return Redis(
        host=redis_url.hostname,
        port=redis_url.port,
        password=redis_url.password or None,
        db=int(redis_url.path.lstrip('/') or 0)
    )

def init_db():
    global db
    return db