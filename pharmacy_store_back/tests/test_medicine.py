import requests

BASE_URL = 'http://localhost:5000'  # 替换为您的后端地址

def register_admin_user():
    # 注册管理员用户
    response = requests.post(f'{BASE_URL}/register', json={
        'username': 'adminuser1',
        'password': 'adminpassword',
        'email': 'adminuser1@example.com',
        'is_admin': 1  # 设置为管理员
    })
    print("Register Admin Response Code:", response.status_code)  # 打印状态码
    print("Register Admin Response JSON:", response.json())  # 打印返回的 JSON 数据

def login_admin_user():
    # 登录管理员用户
    response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser1',
        'password': 'adminpassword',
        'is_admin': 1
    })
    print("Login Admin Response Code:", response.status_code)  # 打印状态码
    print("Login Admin Response JSON:", response.json())  # 打印返回的 JSON 数据
    assert response.status_code == 200  # 假设登录成功返回 200
    return response.json()['token']  # 返回 token

def test_create_medicine():
    # 登录管理员用户
    admin_login_response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser',
        'password': 'adminpassword',
        'is_admin': 1
    })
    admin_token = admin_login_response.json()['token']

    # 准备上传的药品数据
    medicine_data = {
        'name': 'Test Medicine',
        'description': 'This is a test medicine.',
        'price': 10.99,
        'category': 'Pain Relief',
        'is_prescription': False,
        'is_healthcare': False
    }

    # 上传图片
    with open('./med_test.jpg', 'rb') as image_file:  
        files = {'image': image_file}
        response = requests.post(f'{BASE_URL}/medicines', headers={
            'Authorization': f'Bearer {admin_token}'
        }, data=medicine_data, files=files)

    assert response.status_code == 200  # 应返回201
    assert response.json()['message'] == "Medicine added successfully!"
    
def test_edit_medicine():
    # 登录管理员用户
    admin_login_response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser',
        'password': 'adminpassword',
        'is_admin': 1
    })
    admin_token = admin_login_response.json()['token']

    # 假设我们已经有一个药品 ID 为 1 的药品
    medicine_id = 1  # 替换为实际的药品 ID

    # 测试编辑药品
    updated_data = {
        'name': 'Updated Medicine',
        'description': 'This is an updated test medicine.',
        'price': 12.99,
        'category': 'Pain Relief',
        'is_prescription': True,
        'is_healthcare': True
    }

    response = requests.put(f'{BASE_URL}/medicines/{medicine_id}', json=updated_data, headers={
        'Authorization': f'Bearer {admin_token}'
    })

    assert response.status_code == 200  # 假设编辑成功返回 200
    assert response.json()['code'] == 0  # 检查返回的 code
    assert response.json()['msg'] == "Medicine updated successfully!"

def test_delete_medicine():
    # 假设我们已经有一个药品 ID 为 1 的药品
    medicine_id = 1  # 替换为实际的药品 ID
    admin_login_response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser',
        'password': 'adminpassword',
        'is_admin': 1
    })
    admin_token = admin_login_response.json()['token']
    # 测试删除药品
    response = requests.delete(f'{BASE_URL}/medicines/batch-delete', headers={'Authorization': f'Bearer {admin_token}'}, json={'medicine_ids': [medicine_id]})  # 使用管理员 token

    print("Delete Medicine Response Code:", response.status_code)  # 打印状态码
    print("Delete Medicine Response JSON:", response.json())  # 打印返回的 JSON 数据
    
    assert response.status_code == 200  # 假设删除成功返回 200

def test_non_admin_access():
    # 注册普通用户
    response = requests.post(f'{BASE_URL}/register', json={
        'username': 'normaluser',
        'password': 'userpassword',
        'email': 'normaluser@example.com',
        'is_admin': 0  # 设置为普通用户
    })

    # 登录普通用户
    response = requests.post(f'{BASE_URL}/login', json={
        'username': 'normaluser',
        'password': 'userpassword',
        'is_admin': 0
    })
    assert response.status_code == 200  # 假设登录成功返回 200
    normal_user_token = response.json()['token']  # 获取普通用户的 token

    # 测试普通用户创建药品
    response = requests.post(f'{BASE_URL}/medicines', json={
        'name': 'Unauthorized Medicine',
        'description': 'This should not be allowed.',
        'price': 10.99,
        'image': None,
        'sales': 0,
        'is_prescription': False,
        'is_healthcare': False
    }, headers={'Authorization': f'Bearer {normal_user_token}'})  # 使用普通用户 token

    print("Unauthorized Create Medicine Response Code:", response.status_code)  # 打印状态码
    print("Unauthorized Create Medicine Response JSON:", response.json())  # 打印返回的 JSON 数据
    assert response.status_code == 403  # 假设普通用户无法创建药品返回 403

def test_get_medicines():
    # 登录管理员用户
    admin_login_response = requests.post(f'{BASE_URL}/login', json={
        'username': 'adminuser1',
        'password': 'adminpassword',
        'is_admin': 1
    })
    admin_token = admin_login_response.json()['token']

    # 测试获取药品列表
    response = requests.get(f'{BASE_URL}/medicines', headers={
        'Authorization': f'Bearer {admin_token}'
    })

    print("Get Medicines Response Code:", response.status_code)  # 打印状态码
    print("Get Medicines Response JSON:", response.json())  # 打印返回的 JSON 数据

    assert response.status_code == 200  # 假设获取成功返回 200
    assert response.json()['code'] == 0  # 检查返回的 code
    assert 'medicines' in response.json()  # 检查返回的 JSON 中是否包含 medicines 列表

def test_get_medicines_by_ids(token):
    data = {
        "ids": [2, 3]  # 替换为实际的药品 ID
    }
    response = requests.post(f'{BASE_URL}/medicines/ids', json=data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    print("Get Medicines by IDs Response:", response.json())

if __name__ == '__main__':
    register_admin_user()  # 注册管理员用户
    admin_token = login_admin_user()  # 登录管理员用户并获取 token
    #test_create_medicine()  # 测试创建药品
    #test_edit_medicine()  # 测试编辑药品
    #test_delete_medicine()  # 测试删除药品
    test_non_admin_access()  # 测试非管理员用户的访问
    test_get_medicines()  # 测试获取药品列表
    test_get_medicines_by_ids(admin_token)  # 测试通过药品 ID 获取药品信息
    print("All medicine tests passed!") 