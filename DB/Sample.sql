
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: MPZinke DB instance creation for SmartCurtain.  This is what I use—feel free to use it as a template.
-- 	BUGS:
-- 	FUTURE:

USE `SmartCurtain`;


-- MPZinke instance: default length 1000
INSERT INTO `Curtains` (`id`, `length`, `ip_address`, `name`) VALUES (1, 43000, '10.0.0.12', 'Office');
INSERT INTO `Curtains` (`id`, `length`, `ip_address`, `name`) VALUES (2, 34000, '10.0.0.13', 'Bedroom');


INSERT INTO `Options` (`id`, `name`, `description`) VALUES
(1, 'Adafruit Feed', 'Google API connection'),
(2, 'Auto Calibrate', 'Curtain calibrates length if it moves full span of rod'),
(3, 'Auto Correct', 'Curtain corrects its position if unexpected reaches an end point'),
(4, 'Event Prediction', 'Use previous events to determine future events'),
(5, 'Google Calendar Curtain Events', 'Read curtain events from Google Calendar'),
(6, 'Sunrise Open', 'Automatically create events for opening the curtain at sunrise'),
(7, 'Sunset Close', 'Automatically create events for closing the curtain at sunset'),
(8, 'Temperature Setting', 'Set the curtain based on thermostat temperature of room, outside weather & incoming light');


INSERT INTO `CurtainsOptions` (`id`, `Curtains.id`, `Options.id`, `is_on`, `notes`) VALUES
(1, 1, 1, TRUE, NULL),  -- Adafruit Feed
(2, 1, 2, TRUE, NULL),  -- Auto Calibrate
(3, 1, 3, TRUE, NULL),  -- Auto Correct
(4, 1, 4, TRUE, 'Value is for clustering leniency in hours'),  -- Event Prediction
(5, 1, 5, FALSE, NULL),  -- Google Calendar
(6, 1, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
(7, 1, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
(8, 1, 8, FALSE, NULL),  -- Temperature Setting
(9, 2, 1, TRUE, NULL),  -- Adafruit Feed
(10, 2, 2, TRUE, NULL),  -- Auto Calibrate
(11, 2, 3, TRUE, NULL),  -- Auto Correct
(12, 2, 4, TRUE, 'Value is for clustering leniency in hours'),  -- Event Prediction
(13, 2, 5, FALSE, NULL),  -- Google Calendar
(14, 2, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
(15, 2, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
(16, 2, 8, FALSE, NULL);  -- Temperature Setting


INSERT INTO `CurtainsOptionsKeyValues` (`CurtainsOptions.id`, `key`, `value`) VALUES
(1, 'office.curtain-close', 0),  -- Adafruit Feed
(1, 'office.curtain-open', 100),  -- Adafruit Feed
(4, NULL, '1.0'),  -- Event Prediction
(9, 'bedroom.curtain-close', 0),  -- Adafruit Feed
(9, 'bedroom.curtain-open', 100),  -- Adafruit Feed
(12, NULL, '1.0');  -- Event Prediction


-- —————————————————————————————————————————————————— CREATE VIEWS —————————————————————————————————————————————————— --

SET @sql = NULL;
SELECT GROUP_CONCAT(
    DISTINCT CONCAT(
        'max(case when `CurtainsOptions`.`Options.id` = \'',
        `CurtainsOptions`.`Options.id`,
        '\' then `CurtainsOptions`.`is_on` end) \'',
        `Options`.`name`,
        '\' '
    )
)
INTO @sql
FROM `CurtainsOptions`
JOIN `Options` ON `CurtainsOptions`.`Options.id` = `Options`.`id`;

SET @sql = CONCAT(
    'CREATE VIEW `OptionsForCurtains` AS
    SELECT `Curtains`.`name`, ', @sql, ' 
    FROM `CurtainsOptions`
    JOIN `Curtains` ON `CurtainsOptions`.`Curtains.id` = `Curtains`.`id`
    JOIN `Options` ON `CurtainsOptions`.`Options.id` = `Options`.`id`
    GROUP BY `CurtainsOptions`.`Curtains.id`'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
