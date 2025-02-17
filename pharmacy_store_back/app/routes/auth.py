from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.utils import generate_token, decode_token  # 导入 generate_token 方法

auth = Blueprint('auth', __name__)


@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        token = auth_header.split(" ")[1]  # 获取 Bearer 后面的 token
    current_user = decode_token(token)
    user_id = current_user['sub']  # 提取用户 ID
    is_admin = current_user['is_admin']  # 提取用户类型
    print(f'当前用户是：{current_user}')
    return jsonify(logged_in_as={'user_id': user_id, 'is_admin': is_admin}), 200


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin')

    user = User.query.filter_by(username=username).first()
    
    if user.is_admin == is_admin:
        if user and check_password_hash(user.password, password):
            token = generate_token(user)  # 使用 utils 中的 generate_token 方法
            print(f'用户：{user.username}登陆，token: {token}')
            return jsonify({'code': 0, 'token': token, 'user': {'username': user.username, 'is_admin': user.is_admin}}), 200
    else:
        return jsonify({'code': 2, 'message': '用户类型不匹配'}), 200
    return jsonify({'code': 1, 'message': '用户名或密码错误'}), 200

@auth.route('/logout', methods=['POST'])
def logout():
    # JWT 注销通常不需要在服务器端处理，因为 JWT 是无状态的
    return jsonify({"code": 0, "message": "Logout successful!"}), 200

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"code": 1, "message": "Username already exists."}), 200

    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        email=data['email'],
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        is_admin=data.get('is_admin', 0)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"code": 0, "message": "User registered successfully!"}), 200

@auth.route('/refresh', methods=['POST'])
@jwt_required()
def token_refresh():
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        token = auth_header.split(" ")[1]  # 获取 Bearer 后面的 token
    current_user = decode_token(token)
    user = User.query.filter_by(id=current_user['sub']).first()
    new_access_token = generate_token(user)  # 生成新的访问 token
    return jsonify(access_token=new_access_token), 200 

@auth.route('/user/profile', methods=['GET'])
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

@auth.route('/user/profile', methods=['PUT'])
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

@auth.route('/user/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 1, "message": "User not found."}), 404

    # 这里假设您有一个发送邮件的函数 send_email
    new_password = "new_password"  # 生成新密码的逻辑
    user.password = generate_password_hash(new_password)
    db.session.commit()

    # send_email(user.email, "Password Reset", f"Your new password is: {new_password}")
    return jsonify({"code": 0, "message": "Password reset successfully! Please check your email."}), 200


