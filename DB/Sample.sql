
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: MPZinke DB instance creation for SmartCurtain.  This is what I use—feel free to use it as a template.
-- 	BUGS:
-- 	FUTURE:


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


INSERT INTO "Homes" ("name") VALUES
('Home');


INSERT INTO "HomesOptions" ("Homes.id", "Options.id", "is_on", "data", "notes")
SELECT "Homes"."id", "Options"."id", "Temp"."is_on", "Temp"."data", "Temp"."notes"
FROM 
(
	VALUES
	('Home', 'Voice Assistant',     FALSE, NULL,                            ''),  -- Voice Assistant
	('Home', 'Auto Calibrate',      FALSE, NULL,                            ''),  -- Auto Calibrate
	('Home', 'Auto Correct',        FALSE, NULL,                            ''),  -- Auto Correct
	('Home', 'Event Prediction',    FALSE, JSON '{"leniency": "01:00:00"}', 'Value is for clustering leniency'),  -- Event Prediction
	('Home', 'Calendar Events',     FALSE, NULL,                            ''),  -- Google Calendar
	('Home', 'Sunrise Open',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
	('Home', 'Sunset Close',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
	('Home', 'Temperature Setting', FALSE, NULL,                            '')
) AS "Temp"("Homes.name", "Options.name", "is_on", "data", "notes")
JOIN "Options" ON "Temp"."Options.name" = "Options"."name"
JOIN "Homes" ON "Temp"."Homes.name" = "Homes"."name";


INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "Temp"."name", "Homes"."id"
FROM
(
	VALUES
	('Home', 'Bedroom'),
	('Home', 'Livingroom')
) AS "Temp"("Homes.name", "name")
JOIN "Homes" ON "Temp"."Homes.name" = "Homes"."name";


-- Used to override HomesOptions
INSERT INTO "RoomsOptions" ("Rooms.id", "Options.id", "is_on", "data", "notes")
SELECT "Rooms"."id", "Options"."id", "Temp"."is_on", "Temp"."data", "Temp"."notes"
FROM 
(
	VALUES
	('Bedroom', 'Voice Assistant',     FALSE, NULL,                            ''),  -- Voice Assistant
	('Bedroom', 'Auto Calibrate',      FALSE, NULL,                            ''),  -- Auto Calibrate
	('Bedroom', 'Auto Correct',        FALSE, NULL,                            ''),  -- Auto Correct
	('Bedroom', 'Event Prediction',    FALSE, JSON '{"leniency": "01:00:00"}', 'Value is for clustering leniency'),  -- Event Prediction
	('Bedroom', 'Calendar Events',     FALSE, NULL,                            ''),  -- Google Calendar
	('Bedroom', 'Sunrise Open',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunrise that curtain opens'),  -- Sunrise Open
	('Bedroom', 'Sunset Close',        FALSE, JSON '{"city": "DALLAS"}',       'Value is for time before/after sunset that curtain closes'),  -- Sunset Close
	('Bedroom', 'Temperature Setting', FALSE, NULL,                            '')   -- Temperature Setting
) AS "Temp"("Rooms.name", "Options.name", "is_on", "data", "notes")
JOIN "Options" ON "Temp"."Options.name" = "Options"."name"
JOIN "Rooms" ON "Temp"."Rooms.name" = "Rooms"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "Temp"."name", "Rooms"."id"
FROM
(
	VALUES
	('Bedroom', 'Bedroom-Curtain'),
	('Livingroom', 'Livingroom-Curtain')
) AS "Temp"("Rooms.name", "name")
JOIN "Rooms" ON "Temp"."Rooms.name" = "Rooms"."name";


-- Used to override RoomsOptions
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


INSERT INTO "CurtainsEvents" ("Curtains.id", "percentage") VALUES
(1, 0);
