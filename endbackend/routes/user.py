from flask import Blueprint, request, jsonify
from models import db, User
from utils.decorators import validate_params
from models.partner_request import PartnerRequest
from datetime import datetime  # 添加datetime导入

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# 更新用户信息
@user_bp.route('/info', methods=['PUT'])
@validate_params(['id'])
def update_user():
    data = request.get_json()
    user = User.query.get(data['id'])
    
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    
    # 检查账号是否被修改，如果修改了，需要验证新账号是否可用
    if 'account' in data and data['account'] != user.account:
        # 检查新账号是否已存在
        existing_user = User.query.filter_by(account=data['account']).first()
        if existing_user:
            return jsonify({"message": "账号不可使用，已被占用", "status": "error"}), 400
        user.account = data['account']
    
    # 更新用户信息
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        if len(data['password']) < 6:
            return jsonify({"message": "密码长度至少为6位", "status": "error"}), 400
        user.password = data['password']
    if 'identity' in data:
        if data['identity'] not in ['消费者', '商户', '农户']:
            return jsonify({"message": "身份类型无效", "status": "error"}), 400
        user.identity = data['identity']
    
    try:
        db.session.commit()
        return jsonify({
            "message": "更新成功",
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "account": user.account,
                "identity": user.identity
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"更新失败: {str(e)}", "status": "error"}), 500

# 获取用户列表
@user_bp.route('/list', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id,
        'username': user.username,
        'account': user.account,
        'identity': user.identity
    } for user in users]
    
    return jsonify({
        "message": "获取用户列表成功",
        "status": "success",
        "data": user_list
    })

# 搜索用户
@user_bp.route('/search', methods=['GET'])
@validate_params(['keyword', 'current_user_id'])
def search_users():
    keyword = request.args.get('keyword')
    current_user_id = int(request.args.get('current_user_id'))
    
    # 获取当前用户信息
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({"message": "当前用户不存在", "status": "error"}), 404
    
    # 根据用户身份确定搜索条件
    if current_user.identity == '商户':
        # 商户只能搜索农户
        users = User.query.filter(
            User.identity == '农户',
            User.username.like(f'%{keyword}%')  # 只通过username搜索
        ).all()
    elif current_user.identity == '农户':
        # 农户只能搜索商户
        users = User.query.filter(
            User.identity == '商户',
            User.username.like(f'%{keyword}%')  # 只通过username搜索
        ).all()
    else:
        return jsonify({"message": "只有商户和农户可以搜索合作伙伴", "status": "error"}), 403
    
    # 获取当前用户的合作伙伴ID列表
    partner_ids = []
    if current_user.worktogeter:
        partner_ids = [int(id) for id in current_user.worktogeter.split(',')]
    
    # 获取已发送的请求
    sent_requests = PartnerRequest.query.filter_by(sender_id=current_user_id).all()
    sent_request_receiver_ids = [req.receiver_id for req in sent_requests]
    
    # 构建用户列表，并标记状态
    user_list = []
    for user in users:
        status = 'none'  # 默认状态
        if user.id in partner_ids:
            status = 'partner'  # 已是合作伙伴
        elif user.id in sent_request_receiver_ids:
            # 查找请求状态
            request_obj = next((req for req in sent_requests if req.receiver_id == user.id), None)
            if request_obj:
                status = request_obj.status  # pending, accepted, rejected
        
        user_list.append({
            'id': user.id,
            'username': user.username,
            'account': user.account,
            'identity': user.identity,
            'status': status
        })
    
    return jsonify({
        "message": "搜索用户成功",
        "status": "success",
        "data": user_list
    })

# 添加合作伙伴
@user_bp.route('/partner/add', methods=['POST'])
@validate_params(['user_id', 'partner_id'])
def add_partner():
    data = request.get_json()
    user_id = data['user_id']
    partner_id = data['partner_id']
    
    # 获取用户和合作伙伴信息
    user = User.query.get(user_id)
    partner = User.query.get(partner_id)
    
    if not user or not partner:
        return jsonify({"message": "用户或合作伙伴不存在", "status": "error"}), 404
    
    # 验证身份匹配
    valid_partnership = (
        (user.identity == '商户' and partner.identity == '农户') or
        (user.identity == '农户' and partner.identity == '商户')
    )
    
    if not valid_partnership:
        return jsonify({"message": "只能在商户和农户之间建立合作关系", "status": "error"}), 400
    
    # 添加合作伙伴ID到用户的worktogeter字段
    partner_ids = []
    if user.worktogeter:
        partner_ids = user.worktogeter.split(',')
    
    # 检查是否已经是合作伙伴
    if str(partner_id) in partner_ids:
        return jsonify({"message": "已经是合作伙伴", "status": "error"}), 400
    
    partner_ids.append(str(partner_id))
    user.worktogeter = ','.join(partner_ids)
    
    try:
        db.session.commit()
        return jsonify({
            "message": "添加合作伙伴成功",
            "status": "success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"添加合作伙伴失败: {str(e)}", "status": "error"}), 500

# 删除合作伙伴
@user_bp.route('/partner/remove', methods=['POST'])
@validate_params(['user_id', 'partner_id'])
def remove_partner():
    data = request.get_json()
    user_id = data['user_id']
    partner_id = data['partner_id']
    
    # 获取用户信息
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    
    # 从用户的worktogeter字段中移除合作伙伴ID
    if user.worktogeter:
        partner_ids = user.worktogeter.split(',')
        if str(partner_id) in partner_ids:
            partner_ids.remove(str(partner_id))
            user.worktogeter = ','.join(partner_ids) if partner_ids else None
            
            try:
                db.session.commit()
                return jsonify({
                    "message": "删除合作伙伴成功",
                    "status": "success"
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": f"删除合作伙伴失败: {str(e)}", "status": "error"}), 500
    
    return jsonify({"message": "该用户不是您的合作伙伴", "status": "error"}), 400

# 获取合作伙伴列表
@user_bp.route('/partners', methods=['GET'])
@validate_params(['user_id'])
def get_partners():
    user_id = request.args.get('user_id')
    
    # 获取用户信息
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    
    # 获取合作伙伴列表
    partner_list = []
    if user.worktogeter:
        partner_ids = user.worktogeter.split(',')
        partners = User.query.filter(User.id.in_(partner_ids)).all()
        
        partner_list = [{
            'id': partner.id,
            'username': partner.username,
            'account': partner.account,
            'identity': partner.identity
        } for partner in partners]
    
    return jsonify({
        "message": "获取合作伙伴列表成功",
        "status": "success",
        "data": partner_list
    })

# 发送合作伙伴请求
# 发送合作伙伴请求
@user_bp.route('/partner/request', methods=['POST'])
@validate_params(['user_id', 'partner_id'])
def send_partner_request():
    data = request.get_json()
    user_id = data['user_id']
    partner_id = data['partner_id']
    
    # 获取用户和合作伙伴信息
    user = User.query.get(user_id)
    partner = User.query.get(partner_id)
    
    if not user or not partner:
        return jsonify({"message": "用户或合作伙伴不存在", "status": "error"}), 404
    
    # 验证身份匹配
    valid_partnership = (
        (user.identity == '商户' and partner.identity == '农户') or
        (user.identity == '农户' and partner.identity == '商户')
    )
    
    if not valid_partnership:
        return jsonify({"message": "只能在商户和农户之间建立合作关系", "status": "error"}), 400
    
    # 检查是否已经是合作伙伴
    if user.worktogeter and str(partner_id) in user.worktogeter.split(','):
        return jsonify({"message": "已经是合作伙伴", "status": "error"}), 400
    
    # 检查是否已经发送过请求
    existing_request = PartnerRequest.query.filter_by(
        sender_id=user_id, 
        receiver_id=partner_id,
        status='pending'
    ).first()
    
    if existing_request:
        return jsonify({"message": "已经发送过请求，等待对方确认", "status": "error"}), 400
    
    # 获取当前时间
    current_time = datetime.now()
    
    # 创建新的合作伙伴请求
    new_request = PartnerRequest(
        sender_id=user_id,
        receiver_id=partner_id,
        created_at=current_time,  # 手动设置创建时间
        updated_at=current_time   # 手动设置更新时间
    )
    
    try:
        db.session.add(new_request)
        db.session.commit()
        return jsonify({
            "message": "合作请求已发送，等待对方确认",
            "status": "success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"发送合作请求失败: {str(e)}", "status": "error"}), 500

# 获取收到的合作伙伴请求
@user_bp.route('/partner/requests/received', methods=['GET'])
@validate_params(['user_id'])
def get_received_requests():
    user_id = request.args.get('user_id')
    
    # 获取用户信息
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "用户不存在", "status": "error"}), 404
    
    # 获取收到的待处理请求
    requests = PartnerRequest.query.filter_by(
        receiver_id=user_id,
        status='pending'
    ).all()
    
    request_list = []
    for req in requests:
        sender = User.query.get(req.sender_id)
        if sender:
            request_list.append({
                'request_id': req.id,
                'sender_id': sender.id,
                'sender_username': sender.username,
                'sender_account': sender.account,
                'sender_identity': sender.identity,
                'created_at': req.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return jsonify({
        "message": "获取合作请求成功",
        "status": "success",
        "data": request_list
    })

# 处理合作伙伴请求
# 处理合作伙伴请求
@user_bp.route('/partner/request/respond', methods=['POST'])
@validate_params(['request_id', 'user_id', 'action'])
def respond_to_request():
    data = request.get_json()
    request_id = data['request_id']
    user_id = data['user_id']
    action = data['action']  # 'accept' 或 'reject'
    
    if action not in ['accept', 'reject']:
        return jsonify({"message": "无效的操作", "status": "error"}), 400
    
    # 获取请求信息
    partner_request = PartnerRequest.query.get(request_id)
    if not partner_request:
        return jsonify({"message": "请求不存在", "status": "error"}), 404
    
    # 验证接收者身份
    if partner_request.receiver_id != int(user_id):
        return jsonify({"message": "无权处理此请求", "status": "error"}), 403
    
    # 手动更新updated_at字段
    partner_request.updated_at = datetime.now()
    
    # 处理请求
    if action == 'accept':
        # 更新请求状态
        partner_request.status = 'accepted'
        
        # 获取发送者和接收者
        sender = User.query.get(partner_request.sender_id)
        receiver = User.query.get(partner_request.receiver_id)
        
        # 更新双方的合作伙伴列表
        # 更新发送者的合作伙伴列表
        sender_partners = []
        if sender.worktogeter:
            sender_partners = sender.worktogeter.split(',')
        if str(receiver.id) not in sender_partners:
            sender_partners.append(str(receiver.id))
            sender.worktogeter = ','.join(sender_partners)
        
        # 更新接收者的合作伙伴列表
        receiver_partners = []
        if receiver.worktogeter:
            receiver_partners = receiver.worktogeter.split(',')
        if str(sender.id) not in receiver_partners:
            receiver_partners.append(str(sender.id))
            receiver.worktogeter = ','.join(receiver_partners)
        
        message = "已接受合作请求"
    else:  # reject
        partner_request.status = 'rejected'
        message = "已拒绝合作请求"
    
    try:
        db.session.commit()
        return jsonify({
            "message": message,
            "status": "success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"处理请求失败: {str(e)}", "status": "error"}), 500