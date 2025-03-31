from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.utils import generate_token, decode_token  # 导入 generate_token 方法

auth = Blueprint('auth', __name__)


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







