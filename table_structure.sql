-- Adminer 4.8.1 MySQL 5.7.42-0ubuntu0.18.04.1 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `passwords`;
CREATE TABLE `passwords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service` varchar(100) NOT NULL,
  `identifiant` varchar(100) DEFAULT NULL,
  `mdp` varchar(2000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- 2024-01-13 13:09:36
