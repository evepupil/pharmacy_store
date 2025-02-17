from flask_sqlalchemy import SQLAlchemy

from app import db

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='cart_items')
    medicine = db.relationship('Medicine', backref='cart_items')

    def __repr__(self):
        return f'<Cart {self.id}>' 