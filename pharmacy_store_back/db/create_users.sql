-- db/create_users.sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE  -- 新增字段，默认为普通用户
);