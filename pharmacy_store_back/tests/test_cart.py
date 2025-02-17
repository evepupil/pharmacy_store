import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的后端地址

def register_user(username, password, email):
    response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password,
        'email': email,
        'is_admin': 0  # 默认设置为普通用户
    })
    return response

def login_user(username, password):
    response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password,
        'is_admin': 0  # 默认设置为普通用户
    })
    if response.status_code == 200:
        return response.json()['token']  # 返回 token
    return None

def test_get_cart_items(token):
    response = requests.get(f'{BASE_URL}/cart', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    print("Get Cart Items Response:", response.json())

def test_add_to_cart(token):
    # 假设您要添加的药品 ID 和数量
    data = {
        'medicine_ids': [2],  # 替换为实际的药品 ID
        'quantities': [2]  # 对应的数量
    }
    response = requests.post(f'{BASE_URL}/cart', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    print("Add to Cart Response:", response.json())

def test_delete_cart_items(token):
    # 假设您要删除的购物车商品 ID
    data = {
        'item_ids': [1]  # 替换为实际的购物车商品 ID
    }
    response = requests.delete(f'{BASE_URL}/cart', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    print("Delete Cart Items Response:", response.json())

def test_checkout(token):
    # 假设您要结账的商品
    data = {
        'items': [
            {'medicine_id': 3, 'quantity': 1},  # 替换为实际的药品 ID 和数量
            {'medicine_id': 2, 'quantity': 2}
        ]
    }
    response = requests.post(f'{BASE_URL}/cart/checkout', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    print("Checkout Response:", response.json())

if __name__ == '__main__':
    # 注册用户
    username = 'testuser'
    password = 'testpassword'
    email = 'testuser@example.com'
    register_response = register_user(username, password, email)
    assert register_response.status_code == 200

    # 登录用户并获取 token
    token = login_user(username, password)
    assert token is not None

    # 进行购物车操作
    test_get_cart_items(token)
    test_add_to_cart(token)
    test_delete_cart_items(token)
    #test_checkout(token)
    print("All cart tests passed!") 