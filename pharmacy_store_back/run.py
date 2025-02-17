# pharmacy_store/run.py

from app import create_app

# 创建 Flask 应用实例
app = create_app()

if __name__ == '__main__':
    # 运行应用
    app.run(host='localhost', port=5000, debug=True)
