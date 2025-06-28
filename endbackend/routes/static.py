from flask import Blueprint, send_from_directory
import os
from config import Config

static_bp = Blueprint('static', __name__)

# 添加新的路由处理图片请求
@static_bp.route('/<folder>/<path:filename>')
def serve_image(folder, filename):
    # 只处理特定的图片文件夹
    if folder in ['in', 'grow', 'out', 'quality_inspection_report']:
        return send_from_directory(os.path.join(Config.STATIC_FOLDER, folder), filename)
    return "File not found", 404