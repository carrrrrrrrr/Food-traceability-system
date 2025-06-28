from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import register_routes

def create_app():
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 配置应用
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    
    # 配置跨域
    CORS(app, resources=Config.CORS_RESOURCES)
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册路由
    register_routes(app)
    
    return app

# 创建数据库表
def init_db(app):
    with app.app_context():
        try:
            db.create_all()
            print('数据库表创建成功')
        except Exception as e:
            print(f'数据库初始化错误：{str(e)}')

# 主程序入口
if __name__ == '__main__':
    app = create_app()
    init_db(app)
    app.run(host='0.0.0.0', port=5000, debug=True)