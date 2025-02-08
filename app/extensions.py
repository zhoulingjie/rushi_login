from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis
from urllib.parse import urlparse

db = SQLAlchemy()
login_manager = LoginManager()

def init_cache(app):
    redis_url = urlparse(app.config['REDIS_URL'])
    return Redis(
        host=redis_url.hostname,
        port=redis_url.port,
        password=redis_url.password or None,
        db=int(redis_url.path.lstrip('/') or 0)
    )

cache = None  # 将在create_app中初始化