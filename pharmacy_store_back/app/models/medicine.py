from datetime import datetime
from app import db  # 确保从正确的路径导入

class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    is_new = db.Column(db.Boolean, default=False)
    is_hot = db.Column(db.Boolean, default=False)
    image = db.Column(db.LargeBinary)  # 存储图片数据
    sales = db.Column(db.Integer, default=0)  # 新增销量字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 新增发布时间字段
    is_prescription = db.Column(db.Boolean, default=False)  # 新增处方药字段
    is_healthcare = db.Column(db.Boolean, default=False)  # 新增保健品字段
    stock = db.Column(db.Integer, default=0)  # 新增库存字段

    def __repr__(self):
        return f'<Medicine {self.name}>' 