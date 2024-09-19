CREATE TABLE products(
   id_product INT AUTO_INCREMENT,
   created_at DATETIME NOT NULL,
   update_at DATETIME,
   name VARCHAR(50) NOT NULL,
   price DECIMAL(10,2) NOT NULL,
   description VARCHAR(150),
   origin VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_product),
   UNIQUE(name)
);

CREATE TABLE stocks(
   id_stocks INT AUTO_INCREMENT,
   quantity INT NOT NULL,
   created_at DATETIME,
   update_at DATETIME,
   id_product INT NOT NULL,
   PRIMARY KEY(id_stocks),
   FOREIGN KEY(id_product) REFERENCES products(id_product)
);

CREATE TABLE categories(
   id_category INT AUTO_INCREMENT,
   name VARCHAR(50) NOT NULL,
   description VARCHAR(150),
   id_product INT NOT NULL,
   PRIMARY KEY(id_category),
   UNIQUE(name),
   FOREIGN KEY(id_product) REFERENCES products(id_product)
);

CREATE TABLE suppliers(
   id_supplier INT AUTO_INCREMENT,
   name VARCHAR(50) NOT NULL,
   siret VARCHAR(80) NOT NULL,
   address VARCHAR(150),
   email VARCHAR(50),
   phone VARCHAR(50),
   created_at DATETIME NOT NULL,
   update_at DATETIME,
   PRIMARY KEY(id_supplier),
   UNIQUE(name),
   UNIQUE(siret)
);

CREATE TABLE product_suppliers(
   id_product INT,
   id_supplier INT,
   PRIMARY KEY(id_product, id_supplier),
   FOREIGN KEY(id_product) REFERENCES products(id_product),
   FOREIGN KEY(id_supplier) REFERENCES suppliers(id_supplier)
);


INSERT INTO products (created_at, name, price, description, origin) VALUES
(NOW(),'Café Arabica', 12.99, 'Café de haute qualité avec un goût doux et fruité.', 'Colombie'),
(NOW(),'Café Robusta', 10.99, 'Café fort avec un goût amer, idéal pour les expresso.', 'Vietnam'),
(NOW(),'Café Décaféiné', 11.99, 'Café sans caféine pour une consommation sans stimulant.', 'Brésil');

INSERT INTO stocks (quantity, id_product, created_at) VALUES
(100, 1, NOW()),
(50, 2, NOW()),
(75, 3, NOW());

INSERT INTO categories (name, description, id_product) VALUES
('Café Arabica', 'Café de haute qualité avec un goût doux et fruité.', 1),
('Café Robusta', 'Café fort avec un goût amer, idéal pour les expresso.', 2),
('Café Décaféiné', 'Café sans caféine pour une consommation sans stimulant.', 3);

INSERT INTO suppliers (name, siret, address, email, phone, created_at, update_at) VALUES
('Fournisseur A', '12345678901234', '123 Rue de Paris, Paris, France', 'contact@fournisseura.com', '0123456789', NOW(), NOW()),
('Fournisseur B', '23456789012345', '456 Avenue de Lyon, Lyon, France', 'info@fournisseurb.com', '0987654321', NOW(), NOW()),
('Fournisseur C', '34567890123456', '789 Boulevard de Marseille, Marseille, France', 'support@fournisseure.com', '0147258369', NOW(), NOW()),
('Fournisseur D', '45678901234567', '321 Route de Nice, Nice, France', 'sales@fournisseurd.com', '0167894321', NOW(), NOW()),
('Fournisseur E', '56789012345678', '654 Chemin de Bordeaux, Bordeaux, France', 'contact@fournisseure.com', '0176543210', NOW(), NOW());

INSERT INTO product_suppliers (id_product, id_supplier) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 2),
(3, 4);