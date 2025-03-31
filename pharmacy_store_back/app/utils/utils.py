import jwt
import datetime
from flask import current_app

def generate_token(user):
    token = jwt.encode({
        'sub': str(user.id),
        'is_admin': user.is_admin,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 令牌有效期为1天
    }, current_app.config['SECRET_KEY'], algorithm='HS256')  # 使用应用的 SECRET_KEY
    return token 

def decode_token(token):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# 在适当的地方调用 decode_token