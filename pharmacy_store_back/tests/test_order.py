import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的后端地址
def test_login_and_refresh():
    # 1. 登录并获取token
    login_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'is_admin': 0
    }
    login_response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert login_response.status_code == 200

    res = login_response.json()
    access_token = res['token']
    refresh_token = access_token
    print(access_token)
    protected_response = requests.get(f'{BASE_URL}/protected', headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    })


    # 2. 使用refresh_token刷新access_token
    refresh_response = requests.post(f'{BASE_URL}/refresh', headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    print(refresh_response.json())
    assert refresh_response.status_code == 200
    new_access_token = refresh_response.json()['access_token']

    # 3. 验证新生成的access_token是否有效
    protected_response = requests.get(f'{BASE_URL}/protected', headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {new_access_token}'
    })

    assert protected_response.status_code == 200
    return new_access_token

def register_user(username, password, email, is_admin):
    response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password,
        'email': email,
        'is_admin': is_admin
    })
    return response

def login_user(username, password):
    response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password,
        'is_admin': 0  # 假设普通用户
    })
    return response.json()['token'] if response.status_code == 200 else None

def test_get_orders():
    # 注册用户
    register_user('testuser', 'testpassword', 'testuser@example.com', False)
    
    # # 登录用户并获取 token
    # token = login_user('testuser', 'testpassword')
    # assert token is not None, "User login failed, token not received."

    # 测试刷新token
    token = test_login_and_refresh()
    # 测试
    response = requests.get(f'{BASE_URL}/protected', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200  # 假设获取成功返回 200
    
    # 获取用户的订单
    response = requests.get(f'{BASE_URL}/orders', headers={'Authorization': f'Bearer {token}'})
    
    print("Get Orders Response Code:", response.status_code)  # 打印状态码
    print("Get Orders Response JSON:", response.json())  # 打印返回的 JSON 数据
    
    assert response.status_code == 200  # 假设获取成功返回 200

if __name__ == '__main__':
    test_get_orders()
    print("All order tests passed!") 