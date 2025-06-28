from . import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)  # 添加unique=True
    account = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    identity = db.Column(db.Enum('消费者', '商户', '农户'), nullable=False)
    worktogeter = db.Column(db.String(255))  # 添加合作伙伴字段，存储以逗号分隔的ID
    
    def verify_password(self, password):
        return self.password == password  # 直接比较明文密码