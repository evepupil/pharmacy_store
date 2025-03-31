from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"code": 1, "message": "Access denied."}), 200  
    users = User.query.all()  
    return jsonify({
        "code": 0,
        "users": [{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "is_admin": user.is_admin  
        } for user in users]
    }), 200 

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user.is_admin:
        return jsonify({"code": 2, "message": "Access denied."}), 200 
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"code": 0, "message": "User deleted successfully!"}), 200
    return jsonify({"code": 1, "message": "User not found."}), 200

@user_bp.route('/user/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user_id = get_jwt_identity()  
    user = User.query.get(current_user_id) 

    if not user:
        return jsonify({"code": 1, "message": "用户未找到"}), 200

    data = request.get_json() 
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # 验证原密码
    if not check_password_hash(user.password, old_password):
        return jsonify({"code": 2, "message": "原密码错误"}), 200

    # 更新密码
    user.password = generate_password_hash(new_password) 
    db.session.commit()  

    return jsonify({"code": 0, "message": "密码重置成功"}), 200 

@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({
            "code": 0,
            "user": {
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "isAdmin": user.is_admin,
            }
        }), 200
    return jsonify({"code": 1, "message": "User not found."}), 200

@user_bp.route('/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 1, "message": "User not found."}), 200

    data = request.get_json()
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    db.session.commit()

    return jsonify({"code": 0, "message": "User profile updated successfully!"}), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)

    if not user:
        return jsonify({"code": 2, "message": "User not found."}), 200  

    # 检查当前用户是否为管理员
    if not current_user.is_admin:
        return jsonify({"code": 1, "message": "Admin access required."}), 200  # 需要管理员权限

    data = request.get_json()
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)

    db.session.commit()  
    return jsonify({"code": 0, "message": "User updated successfully!"}), 200  