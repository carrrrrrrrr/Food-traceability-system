import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from config import Config

# 文件上传处理函数
def save_file(file, folder):
    if not file:
        return None
        
    # 生成安全的文件名
    filename = secure_filename(file.filename)
    # 添加时间戳和UUID避免文件名冲突
    unique_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{filename}"
    
    # 确保目录存在
    folder_path = os.path.join(Config.STATIC_FOLDER, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    # 保存文件
    file_path = os.path.join(folder_path, unique_filename)
    file.save(file_path)
    
    # 返回相对路径（用于URL访问）
    return f"/{folder}/{unique_filename}"