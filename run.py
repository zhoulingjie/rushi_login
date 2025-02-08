from app import create_app
from app.extensions import db
from app.models import User
import pymysql
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = create_app()


@app.cli.command("init-db")
def init_db():
    print('start init_db')
    """Initialize the database with all required tables"""
    with app.app_context():
        # 获取数据库连接字符串
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # 创建 SQLAlchemy 引擎
        engine = create_engine(db_uri)

        # 检查数据库是否存在
        if not database_exists(engine.url):
            try:
                # 创建数据库
                create_database(engine.url)
                print("数据库已创建！")
            except Exception as e:
                print(f"创建数据库时出错：{e}")
                return

        # 删除所有表（仅用于开发环境）
        db.drop_all()

        # 创建所有表
        db.create_all()

        # 添加初始数据
        admin = User(
            username='admin',
            role='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')

        normal_user = User(
            username='user',
            role='user',
            email='user@example.com'
        )
        normal_user.set_password('user123')

        db.session.add(admin)
        db.session.add(normal_user)
        db.session.commit()

        print("""
数据库已初始化！
初始用户：
- 管理员：admin/admin123
- 普通用户：user/user123
        """)


if __name__ == '__main__':
    print("App is start running...")
    app.run(debug=True)