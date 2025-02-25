from flask import Blueprint, request, jsonify, current_app
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.medicine import Medicine
from app import db
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.payment import Payment

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart_items():
    current_user = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=current_user).all()
    return jsonify({"code": 0, "cart_items": [{"id": item.id, "user_id": item.user_id, "medicine_id": item.medicine_id, "quantity": item.quantity} for item in cart_items]}), 200

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    current_user = get_jwt_identity()
    medicine_ids = data.get('medicine_ids', [])  # 接受一个物品 ID 数组
    quantities = data.get('quantities', [])  # 接受一个数量数组

    if len(medicine_ids) != len(quantities):
        return jsonify({"code": 1, "message": "Mismatch between medicine IDs and quantities."}), 200

    for medicine_id, quantity in zip(medicine_ids, quantities):
        medicine = Medicine.query.get(medicine_id)
        if not medicine:
            return jsonify({"code": 1, "message": f"Medicine ID {medicine_id} not found."}), 404  # 药品不存在

        if medicine.stock < quantity:
            return jsonify({"code": 2, "message": f"Insufficient stock for medicine ID {medicine_id}."}), 200  # 库存不足

        new_cart_item = Cart(user_id=current_user, medicine_id=medicine_id, quantity=quantity)
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify({"code": 0, "message": "Items added to cart!"}), 200

@cart_bp.route('/cart', methods=['DELETE'])
@jwt_required()
def delete_cart_items():
    data = request.get_json()
    item_ids = data.get('item_ids', [])  # 接受一个物品 ID 数组
    current_user = int(get_jwt_identity())
    deleted_items = []
    for item_id in item_ids:
        cart_item = Cart.query.get(item_id)
        print(cart_item)
        if cart_item and cart_item.user_id == current_user:
            db.session.delete(cart_item)
            deleted_items.append(item_id)
        else:
            return jsonify({"code": 1, "message": "Item not found or not authorized."}), 200
    db.session.commit()
    return jsonify({"code": 0, "message": "Items removed from cart!", "deleted_items": deleted_items}), 200

@cart_bp.route('/cart/checkout', methods=['POST'])
@jwt_required()
def checkout_cart():
    data = request.get_json()
    items_to_checkout = data.get('items', [])
    current_user = get_jwt_identity()
    total_price = 0
    new_order = Order(user_id=current_user, status='Pending', total_price=total_price)
    db.session.add(new_order)

    if len(items_to_checkout) == 0:
        return jsonify({"code": 1, "message": "No items to checkout."}), 200

    for item in items_to_checkout:
        cart_item_id = item['id']
        medicine_id = item['medicine_id']
        quantity = item['quantity']
        medicine = Medicine.query.get(medicine_id)

        if medicine and quantity > 0:
            cart_item = Cart.query.get(cart_item_id)
            if cart_item and cart_item.user_id == int(current_user):
                total_price += medicine.price * quantity
                order_item = OrderItem(order_id=new_order.id, medicine_id=medicine_id, quantity=quantity)
                db.session.add(order_item)
                medicine.stock -= quantity
                db.session.add(medicine)
                cart_item.quantity -= quantity
                if cart_item.quantity <= 0:
                    db.session.delete(cart_item)
                else:
                    db.session.add(cart_item)

    new_order.total_price = total_price
    db.session.commit()

    return jsonify({"code": 0, "message": "Order created successfully!", "order_id": new_order.id}), 200