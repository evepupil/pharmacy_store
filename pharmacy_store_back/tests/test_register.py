import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的后端地址

def test_register_new_user():
    response = requests.post(f'{BASE_URL}/register', json={
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com',
        'is_admin': 0
    })
    
    assert response.status_code == 201  # 假设注册成功返回 201
    assert 'User registered successfully!' in response.text  # 假设返回的消息
    print("Test 'test_register_new_user' passed. User registered successfully.")

def test_register_existing_user():
    # 首先注册用户
    requests.post(f'{BASE_URL}/register', json={
        'username': 'existinguser',
        'password': 'existingpassword',
        'email': 'existinguser@example.com',
        'is_admin': 0
    })
    
    # 尝试再次注册同一用户
    response = requests.post(f'{BASE_URL}/register', json={
        'username': 'existinguser',
        'password': 'existingpassword',
        'email': 'existinguser@example.com',
        'is_admin': 0
    })
    
    print("Response Code:", response.status_code)  # 打印状态码
    print("Response JSON:", response.json())  # 打印返回的 JSON 数据
    
    assert response.status_code == 400  # 应该返回 400
    assert 'Username already exists.' in response.text  # 检查返回的消息
    print("Test 'test_register_existing_user' passed. User already exists.")

if __name__ == '__main__':
    test_register_new_user()
    test_register_existing_user()
    print("All tests passed!") 