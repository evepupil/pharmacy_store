-- db/crete_medicines.sql
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    is_new BOOLEAN DEFAULT FALSE,
    is_hot BOOLEAN DEFAULT FALSE
);