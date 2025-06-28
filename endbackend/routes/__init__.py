def register_routes(app):
    # 导入并注册所有路由蓝图
    from .auth import auth_bp
    from .user import user_bp
    from .ingredient import ingredient_bp
    from .food import food_bp
    from .static import static_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(static_bp)