import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的API基础URL

def test_login_and_refresh():
    # 1. 登录并获取token
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    login_response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert login_response.status_code == 200

    tokens = login_response.json()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    # 2. 使用refresh_token刷新access_token
    refresh_response = requests.post(f'{BASE_URL}/refresh', headers={
        'Authorization': f'Bearer {refresh_token}'
    })

    assert refresh_response.status_code == 200
    new_access_token = refresh_response.json()['access_token']

    # 3. 验证新生成的access_token是否有效
    protected_response = requests.get(f'{BASE_URL}/protected', headers={
        'Authorization': f'Bearer {new_access_token}'
    })

    assert protected_response.status_code == 200
    assert 'This is a protected route.' in protected_response.json()['msg']

test_login_and_refresh()