from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app import db
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

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



@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"code": 0, "user": {"id": user.id, "username": user.username}}), 200  # 返回 200 状态码
    return jsonify({"code": 1, "message": "User not found."}), 200  # 返回 200 状态码

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({"message": "Access denied."}), 403  # 如果不是该用户或管理员，返回403

    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.phone = data.get('phone', user.phone)  # 更新手机号
        user.address = data.get('address', user.address)  # 更新地址
        db.session.commit()
        return jsonify({"message": "User information updated successfully!"}), 200
    return jsonify({"message": "User not found."}), 404

@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    # 获取用户信息
    return jsonify({"message": "User information retrieved successfully!"}), 200

@user_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user_info():
    # 更新用户信息
    data = request.get_json()
    # 处理更新逻辑
    return jsonify({"message": "User information updated successfully!"}), 200 