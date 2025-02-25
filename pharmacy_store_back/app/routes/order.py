from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem
from app.models.medicine import Medicine
from app import db
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())  # 获取当前用户的 ID
    print(f'用户是：{user_id}获取订单列表')
    user_orders = Order.query.filter_by(user_id=user_id).all()  # 获取当前用户的所有订单
    orders_with_items = []

    for order in user_orders:
        order_items = [{
            "medicine_id": item.medicine_id,
            "quantity": item.quantity
        } for item in order.items]
        
        orders_with_items.append({
            "id": order.id,
            "total_price": str(order.total_price),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": order_items  # 返回订单项
        })

    return jsonify({"code": 0, "orders": orders_with_items}), 200

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    medicine_items = data['medicine_items']  # 假设您有一个药品 ID 和数量的列表

    total_price = 0
    new_order = Order(user_id=get_jwt_identity(), status='Pending', total_price=total_price)
    db.session.add(new_order)  # 先添加订单，以便获取订单 ID

    for item in medicine_items:
        medicine_id = item['medicine_id']
        quantity = item['quantity']
        medicine = Medicine.query.get(medicine_id)
        if medicine:
            total_price += medicine.price * quantity  # 计算总价格
            order_item = OrderItem(order_id=new_order.id, medicine_id=medicine_id, quantity=quantity)
            db.session.add(order_item)  # 添加订单项
            medicine.stock -= quantity  # 扣除库存
            db.session.add(medicine)  # 更新药品库存

    new_order.total_price = total_price  # 设置订单总价格
    db.session.commit()

    return jsonify({"code": 0, "message": "Order created successfully!"}), 200

@order_bp.route('/orders/user', methods=['GET'])
@login_required
def get_user_orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()  # 获取当前用户的所有订单
    orders_with_items = []

    for order in user_orders:
        order_items = [{
            "medicine_id": item.medicine_id,
            "quantity": item.quantity
        } for item in order.items]
        
        orders_with_items.append({
            "id": order.id,
            "total_price": str(order.total_price),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": order_items  # 返回订单项
        })

    return jsonify(orders_with_items), 200

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order_items = [{
            "medicine_id": item.medicine_id,
            "quantity": item.quantity
        } for item in order.items]
        return jsonify({
            "code": 0,
            "id": order.id,
            "user_id": order.user_id,
            "total_price": str(order.total_price),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": order_items  # 返回订单项
        }), 200
    return jsonify({"code": 1, "message": "Order not found."}), 404

@order_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order:
        if order.user_id != int(get_jwt_identity()):
            return jsonify({"code": 1, "message": "Access denied."}), 403  # 如果不是该用户，返回403

        # 恢复库存
        for item in order.items:
            medicine = Medicine.query.get(item.medicine_id)
            if medicine:
                medicine.stock += item.quantity  # 恢复库存
                db.session.add(medicine)  # 更新药品库存

        order.status = 'Canceled'  # 更新订单状态
        db.session.commit()
        return jsonify({"code": 0, "message": "Order canceled successfully!"}), 200
    return jsonify({"code": 1, "message": "Order not found."}), 404

@order_bp.route('/orders/<int:order_id>/complete', methods=['POST'])
@jwt_required()
def complete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        if order.user_id != int(get_jwt_identity()):
            return jsonify({"code": 1, "message": "Access denied."}), 403  # 如果不是该用户，返回403

        if order.status == 'Pending':
            order.status = 'Completed'  # 更新订单状态为完成
            db.session.commit()
            return jsonify({"code": 0, "message": "Order completed successfully!"}), 200
        else:
            return jsonify({"code": 1, "message": "Order is not in a pending state."}), 200
    return jsonify({"code": 1, "message": "Order not found."}), 404

@order_bp.route('/orders/batch_delete', methods=['DELETE'])
@jwt_required()
def batch_delete_orders():
    data = request.get_json()
    order_ids = data.get('order_ids', [])
    current_user = int(get_jwt_identity())

    if not order_ids:
        return jsonify({"code": 1, "message": "No orders selected for deletion."}), 200

    deleted_orders = []
    for order_id in order_ids:
        order = Order.query.get(order_id)
        if order and order.user_id == current_user:
            # 删除订单项
            OrderItem.query.filter_by(order_id=order_id).delete()
            # 删除订单
            db.session.delete(order)
            deleted_orders.append(order_id)
        else:
            return jsonify({"code": 1, "message": "Order not found or not authorized."}), 200

    db.session.commit()
    return jsonify({"code": 0, "message": "Orders deleted successfully!", "deleted_orders": deleted_orders}), 200 