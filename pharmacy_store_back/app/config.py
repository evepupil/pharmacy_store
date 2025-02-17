import os
import secrets

class Config:
    secret_key = secrets.token_hex(32)
    secret_key = '27fca1affd174087c9e9bddaad93766967cc57db18f493c5a94169a8b27822ad'
    # 生成一个 32 字节的随机字符串
    print(f'secret_key是：{secret_key}')
    # Flask 配置
    SECRET_KEY = secret_key
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://pharmacy_store:123@39.104.17.54/pharmacy_store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT 配置
    JWT_SECRET_KEY = secret_key  # 用于加密 JWT 的密钥
    JWT_TOKEN_LOCATION = ['headers']  # 指定 JWT 存放的位置
    JWT_HEADER_NAME = 'Authorization'  # JWT 在请求头中的名称
    JWT_HEADER_TYPE = 'Bearer'  # JWT 的类型
    
    
    