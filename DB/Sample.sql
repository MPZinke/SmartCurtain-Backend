
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
(1, 1, 1, TRUE, NULL),
(3, 1, 2, TRUE, NULL),
(4, 1, 3, TRUE, NULL),
(5, 1, 4, TRUE, 'Value is for clustering leniency in hours'),
(6, 1, 5, FALSE, NULL),
(7, 1, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),
(8, 1, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),
(9, 1, 8, FALSE, NULL),
(10, 2, 1, TRUE, NULL),
(12, 2, 2, TRUE, NULL),
(13, 2, 3, TRUE, NULL),
(14, 2, 4, TRUE, 'Value is for clustering leniency in hours'),
(15, 2, 5, FALSE, NULL),
(16, 2, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),
(17, 2, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),
(18, 2, 8, FALSE, NULL);


INSERT INTO `CurtainsOptionsKeyValues` (`CurtainsOptions.id`, `key`, `value`) VALUES
(1, 'office.curtain-close', NULL),
(1, 'office.curtain-open', NULL),
(5, NULL, '1.0'),
(9, 'bedroom.curtain-close', NULL),
(9, 'bedroom.curtain-open', NULL),
(14, NULL, '1.0');
