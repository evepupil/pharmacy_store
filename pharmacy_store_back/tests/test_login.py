import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的后端地址

def test_login_admin():
    # 首先注册管理员用户
    requests.post(f'{BASE_URL}/register', json={
        'username': 'adminuser1',
        'password': 'adminpassword',
        'email': 'adminuser1@example.com',
        'is_admin': 1  # 设置为管理员
    })

    # 测试管理员登录
    response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser1',
        'password': 'adminpassword',
        'is_admin': 1
    })

    print("Response Code:", response.status_code)  # 打印状态码
    print("Response JSON:", response.json())  # 打印返回的 JSON 数据
    
    assert response.status_code == 200  # 假设登录成功返回 200
    assert 'token' in response.json()  # 检查是否返回 token
    assert response.json()['user']['is_admin'] == 1  # 确保用户类型为管理员
    print("Test 'test_login_admin' passed. Admin user logged in successfully.")


def test_login_user():
    # 首先注册普通用户
    requests.post(f'{BASE_URL}/register', json={
        'username': 'normaluser',
        'password': 'userpassword',
        'email': 'normaluser@example.com',
        'is_admin': 0  # 设置为普通用户
    })

    # 测试普通用户登录
    response = requests.post(f'{BASE_URL}/login', json={
        'username': 'normaluser',
        'password': 'userpassword',
        'is_admin': 0
    })

    print("Response Code:", response.status_code)  # 打印状态码
    print("Response JSON:", response.json())  # 打印返回的 JSON 数据
    
    assert response.status_code == 200  # 假设登录成功返回 200
    assert 'token' in response.json()  # 检查是否返回 token
    assert response.json()['user']['is_admin'] == 0  # 确保用户类型为普通用户
    print("Test 'test_login_user' passed. Normal user logged in successfully.")
    


if __name__ == '__main__':
    test_login_admin()
    test_login_user()
    print("All tests passed!") 