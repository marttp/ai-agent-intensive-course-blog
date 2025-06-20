-- Create the 'card_types' table
CREATE TABLE IF NOT EXISTS card_types (
  	card_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	card_type_name VARCHAR(50) NOT NULL,
  	issuer VARCHAR(100) NOT NULL
  );

-- Create the 'customers' table
CREATE TABLE IF NOT EXISTS customers (
  	customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	first_name VARCHAR(255) NOT NULL,
  	last_name VARCHAR(255) NOT NULL,
  	email VARCHAR(255) UNIQUE NOT NULL
  );

-- Create the 'transactions' table
CREATE TABLE IF NOT EXISTS transactions (
  	transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	customer_id INTEGER NOT NULL,
  	card_type_id INTEGER NOT NULL,
  	amount DECIMAL(12, 2) NOT NULL,
  	transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  	merchant_name VARCHAR(255) NOT NULL,
  	FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  	FOREIGN KEY (card_type_id) REFERENCES card_types (card_type_id)
  );

-- Insert data into the 'card_types' table
INSERT INTO card_types (card_type_name, issuer) VALUES
  	('Visa', 'Visa Inc.'),
  	('Mastercard', 'Mastercard Inc.'),
  	('American Express', 'American Express Co.');

-- Insert data into the 'customers' table
INSERT INTO customers (first_name, last_name, email) VALUES
  	('Somchai', 'Jaidee', 'somchai.j@email.com'),
  	('Nirand', 'Suksai', 'nirand.s@email.com'),
  	('Wilai', 'Mankong', 'wilai.m@email.com');

-- Insert data into the 'transactions' table
INSERT INTO transactions (customer_id, card_type_id, amount, merchant_name) VALUES
  	(1, 1, 2899.50, 'Central Department Store'),
  	(2, 2, 1250.00, 'Starbucks Coffee'),
  	(1, 3, 5500.75, 'Big C Supercenter'),
  	(3, 1, 890.25, 'McDonald''s'),
  	(2, 1, 3200.00, 'Siam Paragon'),
  	(3, 2, 1750.80, 'Villa Market');