from .. import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 关联用户表
    balance = db.Column(db.Numeric(10, 2), default=0.00)  # 账户余额

    def __repr__(self):
        return f'<Account {self.id} - User {self.user_id} - Balance {self.balance}>' 