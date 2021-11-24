
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
(2, 1, 2, TRUE, NULL),
(3, 1, 3, TRUE, NULL),
(4, 1, 4, TRUE, 'Value is for clustering leniency in hours'),
(5, 1, 5, FALSE, NULL),
(6, 1, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),
(7, 1, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),
(8, 1, 8, FALSE, NULL),
(9, 2, 1, TRUE, NULL),
(10, 2, 2, TRUE, NULL),
(11, 2, 3, TRUE, NULL),
(12, 2, 4, TRUE, 'Value is for clustering leniency in hours'),
(13, 2, 5, FALSE, NULL),
(14, 2, 6, TRUE, 'Value is for time before/after sunrise that curtain opens'),
(15, 2, 7, TRUE, 'Value is for time before/after sunset that curtain closes'),
(16, 2, 8, FALSE, NULL);


INSERT INTO `CurtainsOptionsKeyValues` (`CurtainsOptions.id`, `key`, `value`) VALUES
(1, 'office.curtain-close', 0),
(1, 'office.curtain-open', 100),
(4, NULL, '1.0'),
(9, 'bedroom.curtain-close', 0),
(9, 'bedroom.curtain-open', 100),
(12, NULL, '1.0');
