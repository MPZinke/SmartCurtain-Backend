
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: MPZinke DB instance creation for SmartCurtain.  This is what I use—feel free to use it as a template.
-- 	BUGS:
-- 	FUTURE:


-- MPZinke instance: default length 1000
INSERT INTO `Curtains` (`length`, `name`) VALUES (1000, 'Office');


INSERT INTO `Options` (`name`, `description`) VALUES
('Adafruit Close Feed', 'Google API Close connection'),
('Adafruit Open Feed', 'Google API Open connection'),
('Auto Calibration', 'Curtain calibrates length if it moves full span of rod'),
('Auto Correct', 'Curtain corrects its position if unexpected reaches an end point'),
('Event Prediction', 'Use previous events to determine future events'),
('Google Calendar Curtain Events', 'Read curtain events from Google Calendar'),
('Sunrise Open', 'Automatically create events for opening the curtain at sunrise'),
('Sunset Close', 'Automatically create events for closing the curtain at sunset'),
('Temperature Setting', 'Set the curtain based on thermostat temperature of room, outside weather & incoming light');


INSERT INTO `CurtainsOptions` (`Curtains.id`, `Options.id`, `is_on`, `key`, `notes`, `value`) VALUES
(1, 1, TRUE, 'office.curtain-close', NULL, NULL),
(1, 2, TRUE, 'office.curtain-open', NULL, NULL),
(1, 3, TRUE, NULL, NULL, NULL),
(1, 4, TRUE, NULL, NULL, NULL),
(1, 5, TRUE, NULL, 'Value is for clustering leniency in hours', '1'),
(1, 6, FALSE, NULL, NULL, NULL),
(1, 7, TRUE, NULL, 'Value is for time before/after sunrise that curtain opens', NULL),
(1, 8, TRUE, NULL, 'Value is for time before/after sunset that curtain closes', NULL),
(1, 9, FALSE, NULL, NULL, NULL);
