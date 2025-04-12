USE task2;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10, 2),
    purchase_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO customers (name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Johnson', 'bob@example.com'),
('Cathy Green', 'cathy@example.com'),
('David Lee', 'david@example.com'),
('Eva Chen', 'eva@example.com');

DELIMITER $$

CREATE PROCEDURE insert_customer_purchases()
BEGIN
  DECLARE i INT DEFAULT 0;
  DECLARE cust_id INT;
  WHILE i < 300 DO
    SET cust_id = FLOOR(1 + RAND() * 5);
    INSERT INTO purchases (customer_id, amount, purchase_date)
    VALUES (
      cust_id,
      ROUND(10 + (RAND() * 490), 2),  -- aount between $10–$500
      CURDATE() - INTERVAL FLOOR(RAND() * 365) DAY
    );
    SET i = i + 1;
  END WHILE;
END$$

DELIMITER ;

CALL insert_customer_purchases();