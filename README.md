# 药店管理系统 (Pharmacy Store Management System)

该项目是一个全栈药店管理系统，分为前端和后端两个部分。系统旨在帮助药店管理药品库存、销售、员工和客户信息。

## 技术栈

### 后端
- Python 3
- Flask 框架
- SQLAlchemy ORM
- JWT 认证
- MySQL 数据库

### 前端
- Vue.js 3
- Element Plus UI 组件库
- Axios HTTP 客户端
- Vue Router

## 系统功能

- 用户认证与权限管理
- 药品管理（添加、编辑、删除、查询）
- 库存管理
- 销售记录
- 报表生成
- 员工管理
- 客户信息管理

## 安装指南

### 后端设置

1. 克隆仓库
```
git clone <repository-url>
```

2. 创建并激活虚拟环境
```
python -m venv myenv
# Windows
myenv\Scripts\activate
# Linux/Mac
source myenv/bin/activate
```

3. 安装依赖
```
cd pharmacy_store_back
pip install -r requirements.txt
```

4. 配置数据库
   - 确保已安装MySQL
   - 在 `app/config.py` 中配置数据库连接

5. 运行后端服务
```
python run.py
```

### 前端设置

1. 安装依赖
```
cd front
npm install
```

2. 运行开发服务器
```
npm run serve
```

3. 构建生产版本
```
npm run build
```

## 使用说明

1. 访问 `http://localhost:8080` 打开前端应用
2. 使用默认管理员账户登录:
   - 用户名: admin
   - 密码: admin123

## 开发者

- [开发者名称]

## 许可证

该项目使用 [许可证名称] 许可证 
