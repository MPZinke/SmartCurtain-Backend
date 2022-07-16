
-- 	Created by: MPZinke
-- 	on 2020.12.19
-- 
-- 	DESCRIPTION: MPZinke DB instance creation for SmartCurtain.  This is what I use—feel free to use it as a template.
-- 	BUGS:
-- 	FUTURE:


-- MPZinke instance: default length 1000
INSERT INTO "Curtains" ("length", "name") VALUES
(43000, 'Livingroom-Curtain'),
(34000, 'Bedroom-Curtain');


INSERT INTO "Options" ("name", "description") VALUES
('Adafruit Feed', 'Google API connection'),
('Auto Calibrate', 'Curtain calibrates length if it moves full span of rod'),
('Auto Correct', 'Curtain corrects its position if unexpected reaches an end point'),
('Event Prediction', 'Use previous events to determine future events'),
('Google Calendar Curtain Events', 'Read curtain events from Google Calendar'),
('Sunrise Open', 'Automatically create events for opening the curtain at sunrise'),
('Sunset Close', 'Automatically create events for closing the curtain at sunset'),
('Temperature Setting', 'Set the curtain based on thermostat temperature of room, outside weather & incoming light');


INSERT INTO "CurtainsOptions" ("Curtains.id", "Options.id", "is_on", "notes", "data")
SELECT "Curtains"."id", "Options"."id", "Temp"."is_on", "Temp"."notes", "Temp"."data"
FROM 
(
	VALUES
	('Livingroom-Curtain', 'Adafruit Feed', TRUE, NULL, '{"office.curtain-close": 0, "office.curtain-open": 100}'),
	('Livingroom-Curtain', 'Auto Calibrate', TRUE, NULL, ''),  -- Auto Calibrate
	('Livingroom-Curtain', 'Auto Correct', TRUE, NULL, ''),  -- Auto Correct
	('Livingroom-Curtain', 'Event Prediction', TRUE, 'Value is for clustering leniency in hours', '1.0'),  -- Event Prediction
	('Livingroom-Curtain', 'Google Calendar Curtain Events', FALSE, NULL, ''),  -- Google Calendar
	('Livingroom-Curtain', 'Sunrise Open', TRUE, 'Value is for time before/after sunrise that curtain opens', ''),  -- Sunrise Open
	('Livingroom-Curtain', 'Sunset Close', TRUE, 'Value is for time before/after sunset that curtain closes', ''),  -- Sunset Close
	('Livingroom-Curtain', 'Temperature Setting', FALSE, NULL, ''),  -- Temperature Setting
	('Bedroom-Curtain', 'Adafruit Feed', TRUE, NULL, '{"bedroom.curtain-close": 0, "bedroom.curtain-open": 100}'),  -- Adafruit Feed
	('Bedroom-Curtain', 'Auto Calibrate', TRUE, NULL, ''),  -- Auto Calibrate
	('Bedroom-Curtain', 'Auto Correct', TRUE, NULL, ''),  -- Auto Correct
	('Bedroom-Curtain', 'Event Prediction', TRUE, 'Value is for clustering leniency in hours', '1.0'),  -- Event Prediction
	('Bedroom-Curtain', 'Google Calendar Curtain Events', FALSE, NULL, ''),  -- Google Calendar
	('Bedroom-Curtain', 'Sunrise Open', TRUE, 'Value is for time before/after sunrise that curtain opens', ''),  -- Sunrise Open
	('Bedroom-Curtain', 'Sunset Close', TRUE, 'Value is for time before/after sunset that curtain closes', ''),  -- Sunset Close
	('Bedroom-Curtain', 'Temperature Setting', FALSE, NULL, '')  -- Temperature Setting
) AS "Temp"("Curtains.name", "Options.name", "is_on", "notes", "data")
JOIN "Options" ON "Temp"."Options.name" = "Options"."name"
JOIN "Curtains" ON "Temp"."Curtains.name" = "Curtains"."name";


-- —————————————————————————————————————————————————— CREATE VIEWS —————————————————————————————————————————————————— --

-- SET @sql = NULL;
-- SELECT GROUP_CONCAT(
--     DISTINCT CONCAT(
--         'max(case when "CurtainsOptions"."Options.id" = ''',
--         "CurtainsOptions"."Options.id",
--         ''' then "CurtainsOptions"."is_on" end) ''',
--         "Options"."name",
--         ''' '
--     )
-- )
-- INTO @sql
-- FROM "CurtainsOptions"
-- JOIN "Options" ON "CurtainsOptions"."Options.id" = "Options"."id";

-- SET @sql = CONCAT(
--     'CREATE VIEW "OptionsForCurtains" AS
--     SELECT "Curtains"."name", ', @sql, ' 
--     FROM "CurtainsOptions"
--     JOIN "Curtains" ON "CurtainsOptions"."Curtains.id" = "Curtains"."id"
--     JOIN "Options" ON "CurtainsOptions"."Options.id" = "Options"."id"
--     GROUP BY "CurtainsOptions"."Curtains.id"'
-- );

-- PREPARE stmt FROM @sql;
-- EXECUTE stmt;
-- DEALLOCATE PREPARE stmt;
