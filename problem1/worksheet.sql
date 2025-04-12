USE task1;

CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    sale_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

DELIMITER $$

INSERT INTO products (id, name, category, price) VALUES 
(1, 'Laptop', 'Electronics', 749.99),
(2, 'Headphones', 'Electronics', 149.99),
(3, 'Smartphone', 'Electronics', 399.99),
(4, 'Shirt', 'Clothing', 29.99),
(5, 'Jeans', 'Clothing', 49.99),
(6, 'Coat', 'Clothing', 89.99),
(7, 'Novel', 'Books', 15.99),
(8, 'Comic', 'Books', 9.99),
(9, 'Cookbook', 'Books', 22.99),
(10, 'Sofa', 'Home', 119.99),
(11, 'Chair', 'Home', 49.99),
(12, 'Lamp', 'Home', 34.99);

-- procedure to add the 1000 sample data into sales
CREATE PROCEDURE insert_sample_sales()
BEGIN
  DECLARE i INT DEFAULT 0;
  WHILE i < 1000 DO
    INSERT INTO sales (product_id, quantity, sale_date)
    VALUES (
        FLOOR(1 + RAND() * 12),  -- random product id 1-12
        FLOOR(1 + RAND() * 5),   -- quantity 1-5
        CURDATE() - INTERVAL FLOOR(RAND() * 365) DAY  -- random sale_date
    );
    SET i = i + 1;
  END WHILE;
END$$

DELIMITER ;

SELECT * FROM products LIMIT 12; 

CALL insert_sample_sales();
