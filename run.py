from app import create_app
from app.extensions import db
from app.models import User

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Initialize the database with all required tables"""
    with app.app_context():
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