CREATE TABLE products(
   id_product INT AUTO_INCREMENT,
   created_at DATETIME NOT NULL,
   name VARCHAR(50) NOT NULL,
   price DECIMAL(10,2) NOT NULL,
   description VARCHAR(150),
   color VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_product),
   UNIQUE(name)
);

CREATE TABLE stocks(
   id_stocks INT AUTO_INCREMENT,
   quantity INT NOT NULL,
   id_product INT NOT NULL,
   PRIMARY KEY(id_stocks),
   FOREIGN KEY(id_product) REFERENCES products(id_product)
);


INSERT INTO products (created_at, name, price, description, color)
VALUES 
('2023-08-30 13:25:32', 'Emily Mraz Jr.', 738.00, 'New range of formal shirts are designed keeping you in mind. With fits and styling that will make you stand apart', 'magenta'),
('2023-08-30 07:29:29', 'Lonnie Schuppe DDS', 753.00, 'The slim & simple Maple Gaming Keyboard from Dev Byte comes with a sleek body and 7- Color RGB LED Back-lighting for smart functionality', 'fuchsia'),
('2023-08-29 14:39:54', 'Clint Boyer', 746.00, 'Andy shoes are designed to keeping in mind durability as well as trends, the most stylish range of shoes & sandals', 'blue'),
('2023-08-30 06:55:20', 'Kottea CK150S', 599.00, 'La Kottea CK150S est une machine expresso polyvalente, mais simple d\'utilisation grâce aux filtres pressurisés et filtre simples fournis.', 'olive'),
('2023-08-30 06:44:19', 'Marianne VonRueden', 154.00, 'New ABC 13 9370, 13.3, 5th Gen CoreA5-8250U, 8GB RAM, 256GB SSD, power UHD Graphics, OS 10 Home, OS Office A & J 2016', 'teal'),
('2023-08-30 02:49:49', 'Dr. Jeanne Streich', 608.00, 'The slim & simple Maple Gaming Keyboard from Dev Byte comes with a sleek body and 7- Color RGB LED Back-lighting for smart functionality', 'tan'),
('2023-08-30 10:53:17', 'Ernestine Willms', 662.00, 'The Football Is Good For Training And Recreational Purposes', 'mint green'),
('2023-08-30 02:05:10', 'Yvonne Fisher', 358.00, 'The Apollotech B340 is an affordable wireless mouse with reliable connectivity, 12 months battery life and modern design', 'mint green'),
('2023-08-30 04:12:31', 'Lynn Skiles', 963.00, 'The slim & simple Maple Gaming Keyboard from Dev Byte comes with a sleek body and 7- Color RGB LED Back-lighting for smart functionality', 'blue'),
('2023-08-29 19:07:33', 'April McDermott', 14.00, 'The Apollotech B340 is an affordable wireless mouse with reliable connectivity, 12 months battery life and modern design', 'orchid');

-- Insert sample data into stocks table
INSERT INTO stocks (quantity, id_product)
VALUES 
(56558, 1),
(65152, 2),
(90214, 3),
(5549, 4),
(25994, 5),
(82498, 6),
(92876, 7),
(68486, 8),
(5563, 9),
(81671, 10);