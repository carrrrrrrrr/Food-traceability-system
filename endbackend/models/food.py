from . import db

# 食品-原料关联表
food_ingredient = db.Table('food_ingredient',
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('amount', db.String(50))
)

class Food(db.Model):
    __tablename__ = 'food'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    prise = db.Column(db.Numeric(10, 2), nullable=False)
    info = db.Column(db.Text)
    poundage = db.Column(db.String(50))
    num = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(255))  # 食品种类，以中文逗号分隔
    cooking_time = db.Column(db.DateTime)  # 制作时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # 建立与User的关系
    user = db.relationship('User', backref=db.backref('foods', lazy=True))
    
    # 建立与Ingredient的多对多关系
    ingredients = db.relationship('Ingredient', secondary=food_ingredient,
                                 backref=db.backref('foods', lazy='dynamic'))