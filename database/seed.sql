-- Default Settings
INSERT INTO settings (key, value) VALUES
('shop_name', 'VOICEBILL TAMIL'),
('shop_address', '123 Main Street, Chennai'),
('phone_number', '9876543210'),
('gst_number', '33ABCDE1234F1Z5'),
('upi_id', 'shop@upi'),
('receipt_width', '80mm'),
('printer_name', 'EPSON_TM'),
('default_language', 'ta-IN');

-- Insert Products
INSERT INTO products (name, category, unit, price, gst_percentage, stock_quantity, minimum_stock) VALUES
('Rice', 'Departmental Store', 'kg', 60, 5, 100, 20),
('Sugar', 'Departmental Store', 'kg', 45, 5, 50, 10),
('Milk', 'Departmental Store', 'packet', 25, 0, 100, 20),
('Biscuit', 'Departmental Store', 'packet', 30, 12, 100, 15),
('Soap', 'Departmental Store', 'piece', 40, 18, 100, 10),
('Shampoo', 'Departmental Store', 'bottle', 150, 18, 50, 5),
('Cooking Oil', 'Departmental Store', 'liter', 120, 5, 40, 10),
('Tea', 'Departmental Store', 'packet', 100, 5, 30, 5),
('Coffee', 'Departmental Store', 'packet', 150, 5, 30, 5),
('Snacks', 'Departmental Store', 'packet', 50, 12, 50, 10),
('Drinks', 'Departmental Store', 'bottle', 40, 12, 60, 10),
('Toothpaste', 'Departmental Store', 'piece', 80, 18, 40, 10),
('Detergent', 'Departmental Store', 'kg', 90, 18, 40, 10),
('Salt', 'Departmental Store', 'kg', 20, 0, 50, 10),
('Spices', 'Departmental Store', 'packet', 60, 5, 40, 10),
('Apple', 'Fruits & Vegetables', 'kg', 180, 0, 50, 10),
('Banana', 'Fruits & Vegetables', 'kg', 60, 0, 40, 10),
('Orange', 'Fruits & Vegetables', 'kg', 100, 0, 30, 10),
('Mango', 'Fruits & Vegetables', 'kg', 150, 0, 20, 10),
('Grapes', 'Fruits & Vegetables', 'kg', 120, 0, 20, 5),
('Tomato', 'Fruits & Vegetables', 'kg', 40, 0, 50, 10),
('Potato', 'Fruits & Vegetables', 'kg', 35, 0, 60, 10),
('Onion', 'Fruits & Vegetables', 'kg', 45, 0, 70, 10),
('Carrot', 'Fruits & Vegetables', 'kg', 60, 0, 30, 5),
('Beans', 'Fruits & Vegetables', 'kg', 80, 0, 20, 5),
('Cabbage', 'Fruits & Vegetables', 'piece', 30, 0, 20, 5),
('Brinjal', 'Fruits & Vegetables', 'kg', 40, 0, 25, 5),
('Spinach', 'Fruits & Vegetables', 'bunch', 15, 0, 40, 10),
('Beetroot', 'Fruits & Vegetables', 'kg', 50, 0, 20, 5),
('Capsicum', 'Fruits & Vegetables', 'kg', 90, 0, 15, 5);

-- Insert Aliases (Sample)
INSERT INTO product_aliases (product_id, alias, language) VALUES
(1, 'rice', 'en'), (1, 'arisi', 'ta'), (1, 'அரிசி', 'ta'),
(2, 'sugar', 'en'), (2, 'sarkarai', 'ta'), (2, 'சர்க்கரை', 'ta'),
(3, 'milk', 'en'), (3, 'paal', 'ta'), (3, 'பால்', 'ta'),
(4, 'biscuit', 'en'), (4, 'biscuit', 'ta'), (4, 'பிஸ்கட்', 'ta'),
(16, 'apple', 'en'), (16, 'apple', 'ta'), (16, 'ஆப்பிள்', 'ta'),
(17, 'banana', 'en'), (17, 'vazhaipazham', 'ta'), (17, 'வாழைப்பழம்', 'ta'),
(21, 'tomato', 'en'), (21, 'thakkali', 'ta'), (21, 'தக்காளி', 'ta'),
(22, 'potato', 'en'), (22, 'urulaikilangu', 'ta'), (22, 'உருளைக்கிழங்கு', 'ta'),
(23, 'onion', 'en'), (23, 'vengayam', 'ta'), (23, 'வெங்காயம்', 'ta'),
(24, 'carrot', 'en'), (24, 'carrot', 'ta'), (24, 'கேரட்', 'ta');
