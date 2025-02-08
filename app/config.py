# app/config.py
class Config:
    # 基础配置
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL配置（开发环境）
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/auth_demo'

    # Redis配置
    REDIS_URL = 'redis://:123456@localhost:6379/0'


class ProductionConfig(Config):
    # 生产环境配置示例
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://prod_user:prod_pass@db.prod.com:3306/prod_db'
    REDIS_URL = 'redis://:prod_redis_pass@redis.prod.com:6379/0'