from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, cache, init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db_instance = init_db()
    db_instance.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app) if hasattr(cache, 'init_app') else None

    # 注册蓝图
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app