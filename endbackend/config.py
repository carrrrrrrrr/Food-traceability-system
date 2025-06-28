import os

class Config:
    # 静态文件夹路径
    STATIC_FOLDER = os.path.dirname(os.path.abspath(__file__))
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'mysql+pymysql://root:cyh123@localhost/vuend?charset=utf8mb4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS配置
    CORS_RESOURCES = {r"/api/*": {"origins": "http://localhost:5173"}}