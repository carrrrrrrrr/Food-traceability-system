from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 导入所有模型以便在创建表时被识别
from .user import User
from .food import Food, food_ingredient
from .ingredient import Ingredient
from .partner_request import PartnerRequest