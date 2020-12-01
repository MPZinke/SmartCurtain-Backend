CREATE DATABASE `curtain`;

USE `curtain`;

DROP TABLE IF EXISTS `Curtains`;
CREATE TABLE IF NOT EXISTS `Curtains`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`is_activated` BOOLEAN NOT NULL DEFAULT FALSE,
	`direction` BOOLEAN NOT NULL DEFAULT FALSE,
	`last_connection` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`length` INT UNSIGNED NOT NULL,
	`name` VARCHAR(32) NOT NULL,
	`position` INT UNSIGNED NOT NULL DEFAULT 0
);


INSERT INTO `Curtains` (`length`, `name`) VALUES (1000, 'Office');


DROP TABLE IF EXISTS `Options`;
CREATE TABLE IF NOT EXISTS `Options`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`description` VARCHAR(256) NOT NULL DEFAULT '',
	`is_current` BOOLEAN NOT NULL DEFAULT TRUE,
	`name` VARCHAR(32) NOT NULL
) CHARSET=utf8;


INSERT INTO `Options` (`name`) VALUES
('Adafruit Close Feed'),
('Adafruit Open Feed'),
('Auto Calibration'),
('Auto Correct'),
('Event Prediction'),
('Google Calendar Curtain Events'),
('Sunrise Open'),
('Sunset Close');


DROP TABLE IF EXISTS `CurtainsOptions`;
CREATE TABLE IF NOT EXISTS `CurtainsOptions`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Options.id` INT NOT NULL,
	FOREIGN KEY (`Options.id`) REFERENCES `Options`(`id`),
	`is_on` BOOLEAN NOT NULL
) CHARSET=utf8;


INSERT INTO `CurtainsOptions` (`Curtains.id`, `Options.id`, `is_on`) VALUES
(1, 1, TRUE),
(1, 2, TRUE),
(1, 3, TRUE),
(1, 4, TRUE),
(1, 5, TRUE),
(1, 6, TRUE),
(1, 7, TRUE),
(1, 8, TRUE);


DROP TABLE IF EXISTS `Events`;
CREATE TABLE IF NOT EXISTS `Events`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Options.id` INT NOT NULL,
	FOREIGN KEY (`Options.id`) REFERENCES `Options`(`id`),
	`event_position` INT UNSIGNED NOT NULL,
	`is_current` BOOLEAN DEFAULT TRUE,
	`time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARSET=utf8;


DROP TABLE IF EXISTS `Errors`;
CREATE TABLE IF NOT EXISTS `Errors`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Curtains.position` INT UNSIGNED NOT NULL,
	`Events.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`Events.id`) REFERENCES `Events`(`id`),
	`error` TEXT DEFAULT NULL,
	`path` TEXT DEFAULT NULL,
	`time` DATETIME DEFAULT CURRENT_TIMESTAMP
) CHARSET=utf8;
