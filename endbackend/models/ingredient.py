from . import db

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(255))  # 原料种类，以中文逗号分隔
    description = db.Column(db.Text)
    farming_time = db.Column(db.DateTime)  # 养殖/种植时间
    production_time = db.Column(db.DateTime)  # 出产时间
    planting_image = db.Column(db.String(255))  # 种植图片路径
    growing_image = db.Column(db.String(255))  # 生长图片路径
    production_image = db.Column(db.String(255))  # 出产图片路径
    quality_report_image = db.Column(db.String(255))  # 质检报告图片路径
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 添加用户外键
    
    # 建立与User的关系
    user = db.relationship('User', backref=db.backref('ingredients', lazy=True))