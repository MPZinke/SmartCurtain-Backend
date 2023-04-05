
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: MPZinke DB instance creation for SmartCurtain.  This is what I use—feel free to use it as a template.
-- 	BUGS:
-- 	FUTURE:


INSERT INTO "Curtains" ("name") VALUES
('All'),
('Bedroom-Curtain'),
('Livingroom-Curtain');


INSERT INTO "Options" ("name", "description") VALUES
('Default', 'The default option for events'),
('Voice Assistant', 'Google API connection'),
('Auto Calibrate', 'Curtain calibrates length if it moves full span of rod'),
('Auto Correct', 'Curtain corrects its position if unexpected reaches an end point'),
('Event Prediction', 'Use previous events to determine future events'),
('Calendar Events', 'Read curtain events from Google Calendar'),
('Sunrise Open', 'Automatically create events for opening the curtain at sunrise'),
('Sunset Close', 'Automatically create events for closing the curtain at sunset'),
('Temperature Setting', 'Set the curtain based on thermostat temperature of room, outside weather & incoming light');


INSERT INTO "CurtainsOptions" ("Curtains.id", "Options.id", "is_on", "data", "notes")
SELECT "Curtains"."id", "Options"."id", "Temp"."is_on", "Temp"."data", "Temp"."notes"
FROM 
(
	VALUES
	('Livingroom-Curtain', 'Voice Assistant',     FALSE, NULL,                            ''),  -- Voice Assistant
	('Livingroom-Curtain', 'Auto Calibrate',      FALSE, NULL,                            ''),  -- Auto Calibrate
	('Livingroom-Curtain', 'Auto Correct',        FALSE, NULL,                            ''),  -- Auto Correct
	('Livingroom-Curtain', 'Event Prediction',    FALSE, JSON '{"leniency": "01:00:00"}', 'Value is for clustering leniency'),  -- Event Prediction
	('Livingroom-Curtain', 'Calendar Events',     FALSE, NULL,                            ''),  -- Google Calendar
	('Livingroom-Curtain', 'Sunrise Open',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
	('Livingroom-Curtain', 'Sunset Close',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
	('Livingroom-Curtain', 'Temperature Setting', FALSE, NULL,                            ''),  -- Temperature Setting
	('Bedroom-Curtain',    'Voice Assistant',     FALSE, NULL,                            ''),  -- Voice Assistant
	('Bedroom-Curtain',    'Auto Calibrate',      FALSE, NULL,                            ''),  -- Auto Calibrate
	('Bedroom-Curtain',    'Auto Correct',        FALSE, NULL,                            ''),  -- Auto Correct
	('Bedroom-Curtain',    'Event Prediction',    FALSE, JSON '{"leniency": "01:00:00"}', 'Value is for clustering leniency'),  -- Event Prediction
	('Bedroom-Curtain',    'Calendar Events',     FALSE, NULL,                            ''),  -- Google Calendar
	('Bedroom-Curtain',    'Sunrise Open',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
	('Bedroom-Curtain',    'Sunset Close',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
	('Bedroom-Curtain',    'Temperature Setting', FALSE, NULL,                            '')   -- Temperature Setting
) AS "Temp"("Curtains.name", "Options.name", "is_on", "data", "notes")
JOIN "Options" ON "Temp"."Options.name" = "Options"."name"
JOIN "Curtains" ON "Temp"."Curtains.name" = "Curtains"."name";
