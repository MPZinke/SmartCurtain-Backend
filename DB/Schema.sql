
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


CREATE DATABASE `SmartCurtain` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;;


USE `SmartCurtain`;


-- Primary table for curtain listing.
-- Details individual curtain setups.
DROP TABLE IF EXISTS `Curtains`;
CREATE TABLE IF NOT EXISTS `Curtains`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`buffer_time` SMALLINT UNSIGNED NOT NULL DEFAULT 0,  -- Curtain travel deci-seconds (prevent event overlap)
	`current_position` INT UNSIGNED NOT NULL DEFAULT 0,
	`direction` BOOLEAN NOT NULL DEFAULT FALSE,
	`ip_address` VARCHAR(15) NOT NULL,
	`is_activated` BOOLEAN NOT NULL DEFAULT FALSE,
	`is_current` BOOLEAN NOT NULL DEFAULT TRUE,
	-- `is_safe`: prevents actions from going to a position it thinks is harmful (EG opening farther while 'fully open')
	`is_safe` BOOLEAN NOT NULL DEFAULT TRUE,
	`is_smart` BOOLEAN NOT NULL DEFAULT TRUE,
	`port` SMALLINT UNSIGNED NOT NULL DEFAULT 80,
	`last_connection` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`length` INT UNSIGNED NOT NULL,
	`name` VARCHAR(32) NOT NULL UNIQUE
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `Options`;
CREATE TABLE IF NOT EXISTS `Options`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`description` VARCHAR(256) NOT NULL DEFAULT '',
	`is_current` BOOLEAN NOT NULL DEFAULT TRUE,
	`name` VARCHAR(32) NOT NULL UNIQUE
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `CurtainsOptions`;
CREATE TABLE IF NOT EXISTS `CurtainsOptions`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Options.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`Options.id`) REFERENCES `Options`(`id`),
	UNIQUE `UNIQUE:CurtainsOptions`(`Curtains.id`, `Options.id`),
	`is_on` BOOLEAN NOT NULL,
	`notes` VARCHAR(256) DEFAULT NULL
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `CurtainsOptionsKeyValues`;
CREATE TABLE IF NOT EXISTS `CurtainsOptionsKeyValues`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`CurtainsOptions.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`CurtainsOptions.id`) REFERENCES `CurtainsOptions`(`id`),
	`is_current` BOOLEAN DEFAULT TRUE,
	`key` VARCHAR(256) DEFAULT NULL,
	`value` VARCHAR(256) DEFAULT NULL
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `CurtainsEvents`;
CREATE TABLE IF NOT EXISTS `CurtainsEvents`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Options.id` INT UNSIGNED DEFAULT NULL,
	FOREIGN KEY (`Options.id`) REFERENCES `Options`(`id`),
	`desired_position` INT UNSIGNED NOT NULL,
	`is_activated` BOOLEAN NOT NULL DEFAULT FALSE,
	`is_current` BOOLEAN NOT NULL DEFAULT TRUE,
	`time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `Errors`;
CREATE TABLE IF NOT EXISTS `Errors`
(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
	`Curtains.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`Curtains.id`) REFERENCES `Curtains`(`id`),
	`Curtains.current_position` INT UNSIGNED NOT NULL,
	`CurtainsEvents.id` INT UNSIGNED NOT NULL,
	FOREIGN KEY (`CurtainsEvents.id`) REFERENCES `CurtainsEvents`(`id`),
	`error` TEXT DEFAULT NULL,
	`path` TEXT DEFAULT NULL,
	`time` DATETIME DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE=utf8mb4_general_ci;
