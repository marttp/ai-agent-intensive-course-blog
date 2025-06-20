-- Create the 'products' table
CREATE TABLE IF NOT EXISTS products (
  	product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	product_name VARCHAR(255) NOT NULL,
  	price DECIMAL(10, 2) NOT NULL
  );

-- Create the 'staff' table
CREATE TABLE IF NOT EXISTS staff (
  	staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	first_name VARCHAR(255) NOT NULL,
  	last_name VARCHAR(255) NOT NULL
  );

-- Create the 'orders' table
CREATE TABLE IF NOT EXISTS orders (
  	order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  	customer_name VARCHAR(255) NOT NULL,
  	staff_id INTEGER NOT NULL,
  	product_id INTEGER NOT NULL,
  	FOREIGN KEY (staff_id) REFERENCES staff (staff_id),
  	FOREIGN KEY (product_id) REFERENCES products (product_id)
  );

-- Insert data into the 'products' table (prices in THB)
INSERT INTO products (product_name, price) VALUES
  	('Laptop', 28999.00),
  	('Keyboard', 4699.00),
  	('Mouse', 1089.00);

-- Insert data into the 'staff' table
INSERT INTO staff (first_name, last_name) VALUES
  	('Somchai', 'Jaidee'),
  	('Nirand', 'Suksai'),
  	('Wilai', 'Mankong');

-- Insert data into the 'orders' table
INSERT INTO orders (customer_name, staff_id, product_id) VALUES
  	('Thanakorn Pimpdee', 1, 1),
  	('Kanokwan Suaynam', 2, 2),
  	('Prasert Rungruang', 1, 3);