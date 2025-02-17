from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
import os
from . import config    
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # 加载配置
    app.config.from_object(config.Config)

    jwt_instance = JWTManager(app)

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 注册蓝图
    from .routes.auth import auth as auth_blueprint
    from .routes.order import order_bp as order_bp
    from .routes.medicine import medicine_bp as medicine_bp
    from .routes.user import user_bp as user_bp
    from .routes.cart import cart_bp as cart_bp
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(order_bp)
    app.register_blueprint(medicine_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(cart_bp)
    # 其他蓝图注册...

    @jwt_instance.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({"msg": "Missing or invalid token."}), 401

    @jwt_instance.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({
            "code": 1,
            "message": "The token has expired."
        }), 401
    
    return app
