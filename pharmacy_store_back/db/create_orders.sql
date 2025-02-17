CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_canceled BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)  -- 假设用户表名为 users
);