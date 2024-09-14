-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 14 sep. 2024 à 10:11
-- Version du serveur : 8.0.31
-- Version de PHP : 8.1.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `product_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id_category` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(150) DEFAULT NULL,
  `id_product` int NOT NULL,
  PRIMARY KEY (`id_category`),
  UNIQUE KEY `name` (`name`),
  KEY `id_product` (`id_product`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id_category`, `name`, `description`, `id_product`) VALUES
(1, 'Café Arabica', 'Café de haute qualité avec un goût doux et fruité.', 0),
(2, 'Café Robusta', 'Café fort avec un goût amer, idéal pour les expresso.', 0),
(3, 'Café Décaféiné', 'Café sans caféine pour une consommation sans stimulant.', 0);

-- --------------------------------------------------------

--
-- Structure de la table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id_product` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `update_at` datetime DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` varchar(150) DEFAULT NULL,
  `origin` varchar(50) NOT NULL,
  PRIMARY KEY (`id_product`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `products`
--

INSERT INTO `products` (`id_product`, `created_at`, `update_at`, `name`, `price`, `description`, `origin`) VALUES
(1, '2024-09-14 12:11:26', NULL, 'Café Arabica', '12.99', 'Café de haute qualité avec un goût doux et fruité.', 'Colombie'),
(2, '2024-09-14 12:11:26', NULL, 'Café Robusta', '10.99', 'Café fort avec un goût amer, idéal pour les expresso.', 'Vietnam'),
(3, '2024-09-14 12:11:26', NULL, 'Café Décaféiné', '11.99', 'Café sans caféine pour une consommation sans stimulant.', 'Brésil');

-- --------------------------------------------------------

--
-- Structure de la table `product_suppliers`
--

DROP TABLE IF EXISTS `product_suppliers`;
CREATE TABLE IF NOT EXISTS `product_suppliers` (
  `id_product` int NOT NULL,
  `id_supplier` int NOT NULL,
  PRIMARY KEY (`id_product`,`id_supplier`),
  KEY `id_supplier` (`id_supplier`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `product_suppliers`
--

INSERT INTO `product_suppliers` (`id_product`, `id_supplier`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 2),
(3, 4);

-- --------------------------------------------------------

--
-- Structure de la table `stocks`
--

DROP TABLE IF EXISTS `stocks`;
CREATE TABLE IF NOT EXISTS `stocks` (
  `id_stocks` int NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `id_product` int NOT NULL,
  PRIMARY KEY (`id_stocks`),
  KEY `id_product` (`id_product`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `stocks`
--

INSERT INTO `stocks` (`id_stocks`, `quantity`, `created_at`, `update_at`, `id_product`) VALUES
(1, 100, '2024-09-14 12:11:26', NULL, 1),
(2, 50, '2024-09-14 12:11:26', NULL, 2),
(3, 75, '2024-09-14 12:11:26', NULL, 3);

-- --------------------------------------------------------

--
-- Structure de la table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE IF NOT EXISTS `suppliers` (
  `id_supplier` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `siret` varchar(80) NOT NULL,
  `address` varchar(150) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_supplier`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `siret` (`siret`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `suppliers`
--

INSERT INTO `suppliers` (`id_supplier`, `name`, `siret`, `address`, `email`, `phone`, `created_at`, `update_at`) VALUES
(1, 'Fournisseur A', '12345678901234', '123 Rue de Paris, Paris, France', 'contact@fournisseura.com', '0123456789', '2024-09-14 12:11:26', '2024-09-14 12:11:26'),
(2, 'Fournisseur B', '23456789012345', '456 Avenue de Lyon, Lyon, France', 'info@fournisseurb.com', '0987654321', '2024-09-14 12:11:26', '2024-09-14 12:11:26'),
(3, 'Fournisseur C', '34567890123456', '789 Boulevard de Marseille, Marseille, France', 'support@fournisseure.com', '0147258369', '2024-09-14 12:11:26', '2024-09-14 12:11:26'),
(4, 'Fournisseur D', '45678901234567', '321 Route de Nice, Nice, France', 'sales@fournisseurd.com', '0167894321', '2024-09-14 12:11:26', '2024-09-14 12:11:26'),
(5, 'Fournisseur E', '56789012345678', '654 Chemin de Bordeaux, Bordeaux, France', 'contact@fournisseure.com', '0176543210', '2024-09-14 12:11:26', '2024-09-14 12:11:26');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
