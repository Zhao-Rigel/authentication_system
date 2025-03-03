from flask import Flask
from flask_talisman import Talisman
from extensions import db, bcrypt
from routes import auth, reset

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 安全设置
    #Talisman(app)

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)

    # 注册蓝图
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(reset.reset_bp)

    import models
    with app.app_context():
        db.create_all()  # 创建数据库

    return app

# 仅在直接运行时执行
if __name__ == '__main__':
    app = create_app()
    #app.run(ssl_context='adhoc')
    app.run()