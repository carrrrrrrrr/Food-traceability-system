from functools import wraps
from flask import request, jsonify

# 请求参数验证装饰器
def validate_params(required_params):
    def decorator(func):
        @wraps(func)  # 保留原始函数的元数据
        def wrapper(*args, **kwargs):
            # 根据请求方法获取参数
            if request.method == 'GET':
                data = request.args
            else:
                data = request.get_json() or {}
                
            missing_params = [param for param in required_params if param not in data]
            if missing_params:
                return jsonify({
                    "message": f"缺少必要参数: {', '.join(missing_params)}",
                    "status": "error"
                }), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator