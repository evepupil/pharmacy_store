import jwt
import datetime
from flask import current_app

def generate_token(user):
    token = jwt.encode({
        'sub': str(user.id),
        'is_admin': user.is_admin,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 令牌有效期为1天
    }, current_app.config['SECRET_KEY'], algorithm='HS256')  # 使用应用的 SECRET_KEY
    print(f'生成的 token: {token}')  # 打印生成的 token
    decode_token(token)
    return token 


def decode_token(token):
    try:
        print(f'解码的token是：{token}')
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        print(f'解码后的 token: {decoded}')  # 打印解码后的内容
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError as e:
        print(e)

# 在适当的地方调用 decode_token