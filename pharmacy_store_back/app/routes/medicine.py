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
    # 获取查询参数
    limit = request.args.get('limit', default=20, type=int)  # 默认每页20条
    index = request.args.get('index', default=0, type=int)  # 默认从第0条开始
    keyword = request.args.get('keyword', default='', type=str)  # 搜索关键字
    category = request.args.get('category', default='', type=str)  # 药品类别
    is_prescription = request.args.get('is_prescription', default=None, type=str)  # 是否为处方药
    is_healthcare = request.args.get('is_healthcare', default=None, type=str)  # 是否为保健品

    # 构建查询
    query = Medicine.query

    # 根据关键字过滤
    if keyword:
        query = query.filter(Medicine.name.like(f'%{keyword}%'))

    # 根据类别过滤
    if category:
        query = query.filter(Medicine.category == category)

    # 根据是否为处方药过滤
    if is_prescription is not None:
        query = query.filter(Medicine.is_prescription == (is_prescription.lower() == 'true'))

    # 根据是否为保健品过滤
    if is_healthcare is not None:
        query = query.filter(Medicine.is_healthcare == (is_healthcare.lower() == 'true'))

    # 分页
    medicines = query.offset(index).limit(limit).all()  # 分页查询

    return jsonify({"code": 0, "medicines": [{
        "id": medicine.id,
        "name": medicine.name,
        "description": medicine.description,
        "price": str(medicine.price),
        "stock": medicine.stock,
        #"image": base64.b64encode(medicine.image).decode('utf-8') if medicine.image else None,
    } for medicine in medicines]}), 200

@medicine_bp.route('/medicines/add', methods=['POST'])
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
    image = request.files.get('image')  # 获取上传的文件

    new_medicine = Medicine(
        name=data['name'],
        category=data['category'],
        description=data['description'],
        price=int(data['price']),
        stock=int(data['stock']),
        is_prescription= False if data.get('is_prescription')== 'false' else True,
        is_healthcare= False if data.get('is_healthcare')== 'false' else True,
    )

    if image:
        new_medicine.image = image.read()  # 存储图片数据

    db.session.add(new_medicine)
    db.session.commit()
    return jsonify({"code": 0, "message": "Medicine added successfully!"}), 200

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
        return jsonify({"code": 1, "msg": "No medicine IDs provided."}), 200  # 返回200 Bad Request

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
        return jsonify({"code": 1, "message": "No medicine IDs provided."}), 200  # 没有提供药品 ID

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

@medicine_bp.route('/medicines/recommendations', methods=['GET'])
def get_recommendations():
    # 获取新品推荐（根据创建时间倒序）
    new_products = Medicine.query.order_by(Medicine.created_at.desc()).limit(5).all()  # 获取最新的5个药品

    # 获取热门推荐（根据销量由高到低，排除销量为0的药品）
    hot_products = Medicine.query.filter(Medicine.sales > 0).order_by(Medicine.sales.desc()).limit(5).all()  # 获取销量最高的5个药品，排除销量为0的药品

    # 构建返回数据
    new_products_data = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
    } for product in new_products]

    hot_products_data = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
    } for product in hot_products]

    return jsonify({
        "code": 0,
        "newMedicines": new_products_data,
        "hotMedicines": hot_products_data,
    }), 200