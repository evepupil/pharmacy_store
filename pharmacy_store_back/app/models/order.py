from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_canceled = db.Column(db.Boolean, default=False)  # 新增字段，表示订单是否被取消

    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)  # 关联订单项

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>' 