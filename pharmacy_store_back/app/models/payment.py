from .. import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 关联用户表
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)  # 关联订单表
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # 支付金额
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())  # 支付时间
    status = db.Column(db.String(50), default='Pending')  # 支付状态

    def __repr__(self):
        return f'<Payment {self.id} - User {self.user_id} - Amount {self.amount}>' 