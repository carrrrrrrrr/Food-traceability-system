from flask import Blueprint, request, jsonify
from models import db, User
from utils.decorators import validate_params

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 注册用户
@auth_bp.route('/register', methods=['POST'])
@validate_params(['username', 'account', 'password', 'identity'])
def register():
    data = request.get_json()
    
    # 验证身份类型
    if data['identity'] not in ['消费者', '商户', '农户']:
        return jsonify({"message": "身份类型无效", "status": "error"}), 400
    
    # 验证密码长度
    if len(data['password']) < 6:
        return jsonify({"message": "密码长度至少为6位", "status": "error"}), 400
    
    # 检查账号是否已存在
    if User.query.filter_by(account=data['account']).first():
        return jsonify({"message": "账号不可使用", "status": "error"}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "用户名已被使用", "status": "error"}), 400
    
    # 创建新用户
    new_user = User(
        username=data['username'],
        account=data['account'],
        identity=data['identity'],
        password=data['password']  # 直接使用明文密码
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "注册成功", 
            "status": "success",
            "data": {
                "id": new_user.id,
                "username": new_user.username,
                "account": new_user.account,
                "identity": new_user.identity
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"注册失败: {str(e)}", "status": "error"}), 500

# 用户登录
@auth_bp.route('/login', methods=['POST'])
@validate_params(['account', 'password'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(account=data['account']).first()
    
    if user and user.verify_password(data['password']):
        return jsonify({
            "message": "登录成功", 
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "account": user.account,
                "identity": user.identity
            }
        })
    
    return jsonify({"message": "账号或密码错误", "status": "error"}), 401