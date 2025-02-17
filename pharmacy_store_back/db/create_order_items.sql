CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 订单项的唯一标识
    order_id INT NOT NULL,               -- 关联的订单 ID
    medicine_id INT NOT NULL,            -- 关联的药品 ID
    quantity INT NOT NULL,                -- 购买的数量
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,  -- 关联订单，删除订单时自动删除相关订单项
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)   -- 关联药品
);