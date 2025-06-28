from flask import Blueprint, request, jsonify
import datetime
from models import db, Food, Ingredient, User, food_ingredient
from utils.decorators import validate_params

food_bp = Blueprint('food', __name__, url_prefix='/api/foods')

# 获取所有食品
@food_bp.route('', methods=['GET'])
def get_foods():
    foods = Food.query.all()
    food_list = []
    
    for food in foods:
        # 获取食品制作商户信息
        user = User.query.get(food.user_id)
        merchant_name = user.username if user else "未知商户"
        
        # 获取原材料信息，包含农户信息
        ingredients_info = []
        for ingredient in food.ingredients:
            # 获取原料的农户信息
            ingredient_user = User.query.get(ingredient.user_id)
            farmer_name = ingredient_user.username if ingredient_user else "未知农户"
            
            ingredients_info.append({
                'id': ingredient.id,
                'name': ingredient.name,
                'type': ingredient.type,
                'description': ingredient.description,
                'farming_time': ingredient.farming_time.isoformat() if ingredient.farming_time else None,
                'production_time': ingredient.production_time.isoformat() if ingredient.production_time else None,
                'planting_image': ingredient.planting_image,
                'growing_image': ingredient.growing_image,
                'production_image': ingredient.production_image,
                'quality_report_image': ingredient.quality_report_image,
                'farmer_name': farmer_name,
                'amount': db.session.query(food_ingredient.c.amount)\
                    .filter(food_ingredient.c.food_id == food.id,
                            food_ingredient.c.ingredient_id == ingredient.id)\
                    .scalar() or ''
            })
        
        food_list.append({
            'id': food.id,
            'name': food.name,
            'prise': float(food.prise),
            'info': food.info,
            'poundage': food.poundage,
            'num': food.num,
            'category': food.category,
            'cooking_time': food.cooking_time.isoformat() if food.cooking_time else None,
            'user_id': food.user_id,
            'merchant_name': merchant_name,
            'ingredients': ingredients_info
        })
    
    return jsonify({
        "message": "获取食品列表成功",
        "status": "success",
        "data": food_list
    })

# 获取用户的食品列表
@food_bp.route('/user', methods=['GET'])
def get_user_foods():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "缺少用户ID", "status": "error"}), 400
    
    foods = Food.query.filter_by(user_id=user_id).all()
    food_list = []
    
    for food in foods:
        # 获取食品的原料信息
        ingredients = [{
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'amount': db.session.query(food_ingredient.c.amount)\
                      .filter(food_ingredient.c.food_id == food.id, 
                              food_ingredient.c.ingredient_id == ingredient.id)\
                      .scalar() or ''
        } for ingredient in food.ingredients]
        
        food_list.append({
            'id': food.id,
            'name': food.name,
            'prise': float(food.prise),
            'info': food.info,
            'poundage': food.poundage,
            'num': food.num,
            'category': food.category,
            'cooking_time': food.cooking_time.isoformat() if food.cooking_time else None,
            'user_id': food.user_id,
            'ingredients': ingredients
        })
    
    return jsonify({
        "message": "获取食品列表成功",
        "status": "success",
        "data": food_list
    })

# 添加食品
@food_bp.route('', methods=['POST'])
@validate_params(['name', 'prise', 'poundage', 'num', 'user_id'])
def add_food():
    data = request.get_json()
    
    # 验证用户是否存在且是商户或农户
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    if user.identity not in ['商户', '农户']:
        return jsonify({"message": "只有商户或农户可以添加食品", "status": "error"}), 403
    
    # 验证价格是否为正数
    try:
        price = float(data['prise'])
        if price <= 0:
            return jsonify({"message": "价格必须为正数", "status": "error"}), 400
    except ValueError:
        return jsonify({"message": "价格格式不正确", "status": "error"}), 400
    
    # 验证库存是否为非负整数
    try:
        num = int(data['num'])
        if num < 0:
            return jsonify({"message": "库存不能为负数", "status": "error"}), 400
    except ValueError:
        return jsonify({"message": "库存格式不正确", "status": "error"}), 400
    
    # 处理制作时间
    cooking_time = None
    if data.get('cooking_time'):
        try:
            cooking_time = datetime.datetime.fromisoformat(data['cooking_time'])
        except ValueError:
            return jsonify({"message": "制作时间格式不正确", "status": "error"}), 400
    
    # 创建新食品
    new_food = Food(
        name=data['name'],
        prise=price,
        info=data.get('info', ''),
        poundage=data['poundage'],
        num=num,
        category=data.get('category', ''),
        cooking_time=cooking_time,
        user_id=data['user_id']
    )
    
    # 处理原料关联
    if 'ingredients' in data and isinstance(data['ingredients'], list):
        # 如果是商户，验证所选原料是否来自合作伙伴
        if user.identity == '商户':
            # 获取合作伙伴ID列表
            partner_ids = []
            if user.worktogeter:
                partner_ids = [int(id) for id in user.worktogeter.split(',')]
            
            for ingredient_data in data['ingredients']:
                ingredient_id = ingredient_data.get('id')
                if ingredient_id:
                    ingredient = Ingredient.query.get(ingredient_id)
                    if not ingredient:
                        continue
                    
                    # 检查原料是否来自合作伙伴
                    ingredient_user = User.query.get(ingredient.user_id)
                    if not ingredient_user or ingredient_user.identity != '农户' or ingredient.user_id not in partner_ids:
                        return jsonify({
                            "message": f"原料 '{ingredient.name}' 不是来自您的合作伙伴，无法添加", 
                            "status": "error"
                        }), 403
                    
                    new_food.ingredients.append(ingredient)
        else:
            # 农户可以添加任何原料
            for ingredient_data in data['ingredients']:
                ingredient_id = ingredient_data.get('id')
                if ingredient_id:
                    ingredient = Ingredient.query.get(ingredient_id)
                    if ingredient:
                        new_food.ingredients.append(ingredient)
    
    try:
        db.session.add(new_food)
        db.session.commit()
        
        # 设置原料用量
        if 'ingredients' in data and isinstance(data['ingredients'], list):
            for ingredient_data in data['ingredients']:
                ingredient_id = ingredient_data.get('id')
                amount = ingredient_data.get('amount', '')
                if ingredient_id:
                    # 更新关联表中的用量
                    db.session.execute(
                        food_ingredient.update()
                        .where(food_ingredient.c.food_id == new_food.id)
                        .where(food_ingredient.c.ingredient_id == ingredient_id)
                        .values(amount=amount)
                    )
            db.session.commit()
        
        # 获取食品的原料信息用于返回
        ingredients = [{
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'amount': db.session.query(food_ingredient.c.amount)\
                      .filter(food_ingredient.c.food_id == new_food.id, 
                              food_ingredient.c.ingredient_id == ingredient.id)\
                      .scalar() or ''
        } for ingredient in new_food.ingredients]
        
        return jsonify({
            "message": "添加食品成功", 
            "status": "success",
            "data": {
                "id": new_food.id,
                "name": new_food.name,
                "prise": float(new_food.prise),
                "info": new_food.info,
                "poundage": new_food.poundage,
                "num": new_food.num,
                "category": new_food.category,
                "cooking_time": new_food.cooking_time.isoformat() if new_food.cooking_time else None,
                "user_id": new_food.user_id,
                "ingredients": ingredients
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"添加食品失败: {str(e)}", "status": "error"}), 500

# 删除食品
@food_bp.route('/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get(food_id)
    if not food:
        return jsonify({"message": "食品不存在", "status": "error"}), 404
    
    # 验证用户权限（只有食品的创建者可以删除）
    user_id = request.args.get('user_id')
    if not user_id or int(user_id) != food.user_id:
        return jsonify({"message": "无权限删除此食品", "status": "error"}), 403
    
    try:
        # 删除食品与原料的关联
        food.ingredients = []
        
        # 删除食品
        db.session.delete(food)
        db.session.commit()
        
        return jsonify({
            "message": "删除食品成功", 
            "status": "success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"删除食品失败: {str(e)}", "status": "error"}), 500

# 修改食品
@food_bp.route('/<int:food_id>', methods=['PUT'])
@validate_params(['name', 'prise', 'poundage', 'num'])
def update_food(food_id):
    data = request.get_json()
    
    food = Food.query.get(food_id)
    if not food:
        return jsonify({"message": "食品不存在", "status": "error"}), 404
    
    # 验证用户权限（只有食品的创建者可以修改）
    user_id = data.get('user_id')
    if not user_id or int(user_id) != food.user_id:
        return jsonify({"message": "无权限修改此食品", "status": "error"}), 403
    
    # 验证价格是否为正数
    try:
        price = float(data['prise'])
        if price <= 0:
            return jsonify({"message": "价格必须为正数", "status": "error"}), 400
    except ValueError:
        return jsonify({"message": "价格格式不正确", "status": "error"}), 400
    
    # 验证库存是否为非负整数
    try:
        num = int(data['num'])
        if num < 0:
            return jsonify({"message": "库存不能为负数", "status": "error"}), 400
    except ValueError:
        return jsonify({"message": "库存格式不正确", "status": "error"}), 400
    
    # 处理制作时间
    cooking_time = None
    if data.get('cooking_time'):
        try:
            cooking_time = datetime.datetime.fromisoformat(data['cooking_time'])
        except ValueError:
            return jsonify({"message": "制作时间格式不正确", "status": "error"}), 400
    
    # 更新食品信息
    food.name = data['name']
    food.prise = price
    food.info = data.get('info', '')
    food.poundage = data['poundage']
    food.num = num
    food.category = data.get('category', '')
    food.cooking_time = cooking_time
    
    # 处理原料关联
    if 'ingredients' in data and isinstance(data['ingredients'], list):
        # 清除现有关联
        food.ingredients = []
        
        # 添加新关联
        for ingredient_data in data['ingredients']:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id:
                ingredient = Ingredient.query.get(ingredient_id)
                if ingredient:
                    food.ingredients.append(ingredient)
    
    try:
        db.session.commit()
        
        # 设置原料用量
        if 'ingredients' in data and isinstance(data['ingredients'], list):
            for ingredient_data in data['ingredients']:
                ingredient_id = ingredient_data.get('id')
                amount = ingredient_data.get('amount', '')
                if ingredient_id:
                    # 更新关联表中的用量
                    db.session.execute(
                        food_ingredient.update()
                        .where(food_ingredient.c.food_id == food.id)
                        .where(food_ingredient.c.ingredient_id == ingredient_id)
                        .values(amount=amount)
                    )
            db.session.commit()
        
        # 获取食品的原料信息用于返回
        ingredients = [{
            'id': ingredient.id,
            'name': ingredient.name,
            'description': ingredient.description,
            'amount': db.session.query(food_ingredient.c.amount)\
                      .filter(food_ingredient.c.food_id == food.id, 
                              food_ingredient.c.ingredient_id == ingredient.id)\
                      .scalar() or ''
        } for ingredient in food.ingredients]
        
        return jsonify({
            "message": "修改食品成功", 
            "status": "success",
            "data": {
                "id": food.id,
                "name": food.name,
                "prise": float(food.prise),
                "info": food.info,
                "poundage": food.poundage,
                "num": food.num,
                "category": food.category,
                "cooking_time": food.cooking_time.isoformat() if food.cooking_time else None,
                "user_id": food.user_id,
                "ingredients": ingredients
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"修改食品失败: {str(e)}", "status": "error"}), 500