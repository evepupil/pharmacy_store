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
    users = User.query.all()
    return jsonify({"code": 0, "users": [{"id": user.id, "username": user.username} for user in users]}), 200  # 返回 200 状态码

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({"message": "Access denied."}), 403  # 如果不是管理员，返回403
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    return jsonify({"message": "User not found."}), 404

@user_bp.route('/user/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user_id = get_jwt_identity()  # 获取当前用户身份
    user = User.query.get(current_user_id)  # 获取用户对象

    if not user:
        return jsonify({"code": 1, "message": "用户未找到"}), 200

    data = request.get_json()  # 获取请求数据
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # 验证原密码
    if not check_password_hash(user.password, old_password):
        return jsonify({"code": 2, "message": "原密码错误"}), 200

    # 更新密码
    user.password = generate_password_hash(new_password)  # 哈希新密码
    db.session.commit()  # 提交更改

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
    return jsonify({"code": 1, "message": "User not found."}), 404

@user_bp.route('/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 1, "message": "User not found."}), 404

    data = request.get_json()
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    db.session.commit()

    return jsonify({"code": 0, "message": "User profile updated successfully!"}), 200