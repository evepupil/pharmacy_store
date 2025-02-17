from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.models.medicine import Medicine
from app.utils.utils import decode_token
from app import db
from datetime import datetime
import base64
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt

medicine_bp = Blueprint('medicine', __name__)
UPLOAD_FOLDER = 'uploads/medicines/'  # 图片存储路径
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@medicine_bp.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()  # 查询所有药品
    return jsonify({"code": 0, "medicines":[{
        "id": medicine.id,
        "name": medicine.name,
        "description": medicine.description,
        "price": str(medicine.price),
        "stock": medicine.stock,
        "image": base64.b64encode(medicine.image).decode('utf-8') if medicine.image else None,
    } for medicine in medicines]}), 200

@medicine_bp.route('/medicines', methods=['POST'])
@jwt_required()
def add_medicine():
    current_user = get_jwt_identity()  # 获取当前用户身份
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        token = auth_header.split(" ")[1]  # 获取 Bearer 后面的 token
    current_user = decode_token(token)
    user_id = current_user['sub']  # 提取用户 ID
    is_admin = current_user['is_admin']  # 提取用户类型

    if is_admin != 1:
        return jsonify({"code": 1, "msg": "Admin access required."}), 403  # 返回403 Forbidden

    data = request.form  # 使用 form 数据
    file = request.files['image']  # 获取上传的文件

    if file:
        image_data = file.read()  # 读取文件数据
        print(f'后端收到的data: {data}')
        new_medicine = Medicine(
            name=data.get('name'),
            category=data.get('category'),
            price=data.get('price'),
            description=data.get('description'),
            image=image_data,  # 存储图片数据
            sales=0,  # 初始销量为0
            created_at=datetime.utcnow(),  # 设置创建时间为当前时间
            is_prescription=True if data.get('is_prescription') == 'True' else False,  # 从请求中获取是否为处方药
            is_healthcare=True if data.get('is_healthcare') == 'True' else False,  # 从请求中获取是否为保健品
            stock=data.get('stock', 0)  # 新增库存字段
        )
        print(f'后端编辑好的data: {new_medicine.is_healthcare}')
        db.session.add(new_medicine)
        db.session.commit()
        return jsonify({"code": 0, "message": "Medicine added successfully!"}), 200
    return jsonify({"code": 1, "message": "No image provided."}), 400 

@medicine_bp.route('/medicines/batch-delete', methods=['DELETE'])
@jwt_required()
def batch_delete_medicines():
    current_user = get_jwt_identity()  # 获取当前用户身份
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        token = auth_header.split(" ")[1]  # 获取 Bearer 后面的 token
    current_user = decode_token(token)
    user_id = current_user['sub']  # 提取用户 ID
    is_admin = current_user['is_admin']  # 提取用户类型

    if is_admin != 1:
        return jsonify({"code": 1, "msg": "Admin access required."}), 403  # 返回403 Forbidden

    data = request.get_json()
    medicine_ids = data.get('medicine_ids', [])  # 获取要删除的药品 ID 列表

    if not medicine_ids:
        return jsonify({"code": 1, "msg": "No medicine IDs provided."}), 400  # 返回400 Bad Request

    # 批量删除药品
    medicines_to_delete = Medicine.query.filter(Medicine.id.in_(medicine_ids)).all()
    if not medicines_to_delete:
        return jsonify({"code": 1, "msg": "No medicines found for the provided IDs."}), 404  # 返回404 Not Found

    for medicine in medicines_to_delete:
        db.session.delete(medicine)  # 删除药品

    db.session.commit()  # 提交更改
    return jsonify({"code": 0, "msg": "Medicines deleted successfully!"}), 200

@medicine_bp.route('/medicines/<int:medicine_id>', methods=['PUT'])
@jwt_required()
def edit_medicine(medicine_id):
    current_user = get_jwt_identity()  # 获取当前用户身份
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        token = auth_header.split(" ")[1]  # 获取 Bearer 后面的 token
    current_user = decode_token(token)
    user_id = current_user['sub']  # 提取用户 ID
    is_admin = current_user['is_admin']  # 提取用户类型

    if is_admin != 1:
        return jsonify({"code": 1, "msg": "Admin access required."}), 403  # 返回403 Forbidden

    # 获取请求数据
    data = request.get_json()

    # 查找要编辑的药品
    medicine = Medicine.query.get(medicine_id)
    if not medicine:
        return jsonify({"code": 2, "msg": "Medicine not found."}), 200  # 返回Not Found

    # 更新药品信息
    medicine.name = data.get('name', medicine.name)  # 更新名称
    medicine.category = data.get('category', medicine.category)  # 更新类别
    medicine.price = data.get('price', medicine.price)  # 更新价格
    medicine.is_prescription = data.get('is_prescription', medicine.is_prescription)  # 更新处方状态
    medicine.is_healthcare = data.get('is_healthcare', medicine.is_healthcare)  # 更新保健品状态
    medicine.stock = data.get('stock', medicine.stock)  # 更新库存

    # 更新图片
    if 'image' in request.files:
        file = request.files['image']
        if file:
            image_data = file.read()  # 读取文件数据
            medicine.image = image_data  # 更新图片数据

    db.session.commit()  # 提交更改
    return jsonify({"code": 0, "msg": "Medicine updated successfully!"}), 200

@medicine_bp.route('/medicines/ids', methods=['POST'])
@jwt_required()
def get_medicines_by_ids():
    data = request.get_json()
    medicine_ids = data.get('ids', [])  # 获取药品 ID 列表

    if not medicine_ids:
        return jsonify({"code": 1, "message": "No medicine IDs provided."}), 400  # 没有提供药品 ID

    medicines = Medicine.query.filter(Medicine.id.in_(medicine_ids)).all()  # 查询药品

    if not medicines:
        return jsonify({"code": 1, "message": "No medicines found for the provided IDs."}), 404  # 未找到药品

    # 构建返回数据
    medicine_data = [{
        "id": medicine.id,
        "name": medicine.name,
        "description": medicine.description,
        "image": base64.b64encode(medicine.image).decode('utf-8') if medicine.image else None,
        "price": str(medicine.price),
        "stock": medicine.stock,
        "is_prescription": medicine.is_prescription,
        "is_healthcare": medicine.is_healthcare,
    } for medicine in medicines]

    return jsonify({"code": 0, "medicines": medicine_data}), 200  # 返回药品信息