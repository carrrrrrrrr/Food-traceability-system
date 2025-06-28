# 食品安全溯源系统
## 项目简介
本项目是一个基于Vue.js和Python Flask的食品安全追溯系统，采用前后端分离架构。系统主要功能包括用户认证、食品信息管理、原料追溯等功能。

## 技术栈
### 前端
- Vue.js
- Vite
- Vue Router
- Axios
### 后端
- Python
- Flask
- SQLAlchemy
## 部署说明
### 前端部署
1. 进入前端项目目录：
```
   cd endwork
 ```
2. 安装依赖：
```
   npm install
```
3. 开发环境运行：
```
 npm run dev
```
4. 生产环境构建：
```
   npm run build
 ```
### 后端部署
1. 进入后端项目目录：
```
  cd endbackend
 ```
2. 创建并激活Python虚拟环境（推荐Python 3.10+）：
```
python -m venv venv
.\venv\Scripts\activate
 ```
3. 安装依赖：
```
pip install -r requirements.txt
 ```
4. 运行后端服务：
```
  python app.py
 ```
### 数据库配置
1. 导入数据库文件：
- 使用MySQL数据库
- 导入 vuend.sql 文件
## 使用说明
### 用户功能
1. 注册/登录：访问系统首页，可以进行用户注册和登录
2. 个人中心：登录后可以查看和修改个人信息
### 合作伙伴
1. 合作申请：可以申请成为合作伙伴
2. 合作管理：查看合作状态和管理合作关系
## 注意事项
1. 确保前后端端口配置正确
2. 数据库连接信息需要在后端配置文件中正确设置
3. 文件上传功能需要确保相关目录具有正确的读写权限
## 系统要求
- Node.js 14.0+
- Python 3.10+
- MySQL 5.7+
- 现代浏览器（Chrome、Firefox、Edge等）
