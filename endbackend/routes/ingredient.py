from flask import Blueprint, request, jsonify
import datetime
from models import db, Ingredient, User
from utils.file_handler import save_file
from utils.decorators import validate_params  # 添加这一行导入装饰器

ingredient_bp = Blueprint('ingredient', __name__, url_prefix='/api/ingredients')

# 获取所有原料
@ingredient_bp.route('', methods=['GET'])
def get_ingredients():
    # 可选的用户ID参数，用于筛选特定用户的原料
    user_id = request.args.get('user_id')
    
    query = Ingredient.query
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    ingredients = query.all()
    ingredient_list = [{
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
        'user_id': ingredient.user_id
    } for ingredient in ingredients]
    
    return jsonify({
        "message": "获取原料列表成功",
        "status": "success",
        "data": ingredient_list
    })

# 添加原料（表单提交，支持文件上传）
@ingredient_bp.route('', methods=['POST'])
def add_ingredient():
    # 验证用户身份
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"message": "缺少用户ID", "status": "error"}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
        
    if user.identity != '农户':
        return jsonify({"message": "只有农户可以添加原料", "status": "error"}), 403
    
    # 获取表单数据
    name = request.form.get('name')
    if not name:
        return jsonify({"message": "缺少原料名称", "status": "error"}), 400
        
    # 处理日期时间
    farming_time = None
    production_time = None
    
    if request.form.get('farming_time'):
        try:
            farming_time = datetime.datetime.fromisoformat(request.form.get('farming_time'))
        except ValueError:
            return jsonify({"message": "养殖时间格式不正确", "status": "error"}), 400
            
    if request.form.get('production_time'):
        try:
            production_time = datetime.datetime.fromisoformat(request.form.get('production_time'))
        except ValueError:
            return jsonify({"message": "出产时间格式不正确", "status": "error"}), 400
    
    # 处理文件上传
    planting_image = None
    growing_image = None
    production_image = None
    quality_report_image = None
    
    if 'planting_image' in request.files:
        planting_image = save_file(request.files['planting_image'], 'in')
        
    if 'growing_image' in request.files:
        growing_image = save_file(request.files['growing_image'], 'grow')
        
    if 'production_image' in request.files:
        production_image = save_file(request.files['production_image'], 'out')
        
    if 'quality_report_image' in request.files:
        quality_report_image = save_file(request.files['quality_report_image'], 'quality_inspection_report')
    
    # 创建新原料
    new_ingredient = Ingredient(
        name=name,
        type=request.form.get('type', ''),
        description=request.form.get('description', ''),
        farming_time=farming_time,
        production_time=production_time,
        planting_image=planting_image,
        growing_image=growing_image,
        production_image=production_image,
        quality_report_image=quality_report_image,
        user_id=user_id
    )
    
    try:
        db.session.add(new_ingredient)
        db.session.commit()
        
        return jsonify({
            "message": "添加原料成功", 
            "status": "success",
            "data": {
                "id": new_ingredient.id,
                "name": new_ingredient.name,
                "type": new_ingredient.type,
                "description": new_ingredient.description,
                "farming_time": new_ingredient.farming_time.isoformat() if new_ingredient.farming_time else None,
                "production_time": new_ingredient.production_time.isoformat() if new_ingredient.production_time else None,
                "planting_image": new_ingredient.planting_image,
                "growing_image": new_ingredient.growing_image,
                "production_image": new_ingredient.production_image,
                "quality_report_image": new_ingredient.quality_report_image,
                "user_id": new_ingredient.user_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"添加原料失败: {str(e)}", "status": "error"}), 500

# 删除原料
@ingredient_bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({"message": "原料不存在", "status": "error"}), 404
    
    # 验证用户权限（只有原料的创建者可以删除）
    user_id = request.args.get('user_id')
    if not user_id or int(user_id) != ingredient.user_id:
        return jsonify({"message": "无权限删除此原料", "status": "error"}), 403
    
    try:
        # 删除原料与食品的关联
        for food in ingredient.foods.all():
            food.ingredients.remove(ingredient)
        
        # 删除原料
        db.session.delete(ingredient)
        db.session.commit()
        
        return jsonify({
            "message": "删除原料成功", 
            "status": "success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"删除原料失败: {str(e)}", "status": "error"}), 500

# 修改原料
@ingredient_bp.route('/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({"message": "原料不存在", "status": "error"}), 404
    
    # 验证用户权限（只有原料的创建者可以修改）
    user_id = request.form.get('user_id')
    if not user_id or int(user_id) != ingredient.user_id:
        return jsonify({"message": "无权限修改此原料", "status": "error"}), 403
    
    # 获取表单数据
    name = request.form.get('name')
    if not name:
        return jsonify({"message": "缺少原料名称", "status": "error"}), 400
    
    # 处理日期时间
    farming_time = None
    production_time = None
    
    if request.form.get('farming_time'):
        try:
            farming_time = datetime.datetime.fromisoformat(request.form.get('farming_time'))
        except ValueError:
            return jsonify({"message": "养殖时间格式不正确", "status": "error"}), 400
            
    if request.form.get('production_time'):
        try:
            production_time = datetime.datetime.fromisoformat(request.form.get('production_time'))
        except ValueError:
            return jsonify({"message": "出产时间格式不正确", "status": "error"}), 400
    
    # 处理文件上传
    if 'planting_image' in request.files and request.files['planting_image'].filename:
        planting_image = save_file(request.files['planting_image'], 'in')
        ingredient.planting_image = planting_image
        
    if 'growing_image' in request.files and request.files['growing_image'].filename:
        growing_image = save_file(request.files['growing_image'], 'grow')
        ingredient.growing_image = growing_image
        
    if 'production_image' in request.files and request.files['production_image'].filename:
        production_image = save_file(request.files['production_image'], 'out')
        ingredient.production_image = production_image
        
    if 'quality_report_image' in request.files and request.files['quality_report_image'].filename:
        quality_report_image = save_file(request.files['quality_report_image'], 'quality_inspection_report')
        ingredient.quality_report_image = quality_report_image
    
    # 更新原料信息
    ingredient.name = name
    ingredient.type = request.form.get('type', '')
    ingredient.description = request.form.get('description', '')
    
    if farming_time:
        ingredient.farming_time = farming_time
    if production_time:
        ingredient.production_time = production_time
    
    try:
        db.session.commit()
        
        return jsonify({
            "message": "修改原料成功", 
            "status": "success",
            "data": {
                "id": ingredient.id,
                "name": ingredient.name,
                "type": ingredient.type,
                "description": ingredient.description,
                "farming_time": ingredient.farming_time.isoformat() if ingredient.farming_time else None,
                "production_time": ingredient.production_time.isoformat() if ingredient.production_time else None,
                "planting_image": ingredient.planting_image,
                "growing_image": ingredient.growing_image,
                "production_image": ingredient.production_image,
                "quality_report_image": ingredient.quality_report_image,
                "user_id": ingredient.user_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"修改原料失败: {str(e)}", "status": "error"}), 500

# 获取合作伙伴的原料
@ingredient_bp.route('/partners', methods=['GET'])
@validate_params(['user_id'])
def get_partner_ingredients():
    user_id = request.args.get('user_id')
    
    # 获取用户信息
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    
    # 检查用户是否是商户
    if user.identity != '商户':
        return jsonify({"message": "只有商户可以查看合作伙伴的原料", "status": "error"}), 403
    
    # 获取合作伙伴ID列表
    partner_ids = []
    if user.worktogeter:
        partner_ids = [int(id) for id in user.worktogeter.split(',')]
    
    # 如果没有合作伙伴，返回空列表
    if not partner_ids:
        return jsonify({
            "message": "暂无合作伙伴的原料",
            "status": "success",
            "data": []
        })
    
    # 获取所有合作伙伴（农户）的原料
    partner_ingredients = Ingredient.query.join(User).filter(
        Ingredient.user_id.in_(partner_ids),
        User.identity == '农户'
    ).all()
    
    # 构建原料列表
    ingredient_list = []
    for ing in partner_ingredients:
        # 获取原料的农户信息
        ing_user = User.query.get(ing.user_id)
        
        ingredient_list.append({
            'id': ing.id,
            'name': ing.name,
            'type': ing.type,
            'description': ing.description,
            'farming_time': ing.farming_time.isoformat() if ing.farming_time else None,
            'production_time': ing.production_time.isoformat() if ing.production_time else None,
            'planting_image': ing.planting_image,
            'growing_image': ing.growing_image,
            'production_image': ing.production_image,
            'quality_report_image': ing.quality_report_image,
            'user_id': ing.user_id,
            'farmer_name': ing_user.username if ing_user else "未知农户"
        })
    
    return jsonify({
        "message": "获取合作伙伴原料列表成功",
        "status": "success",
        "data": ingredient_list
    })