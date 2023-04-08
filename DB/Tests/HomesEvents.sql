

-- ———————————————————————————————————— HOME HAS EVENT,  INSERT HOME @ SAME TIME ———————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home1');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home1 Room1', 'Home1'),
	('Home1 Room2', 'Home1'),
	('Home1 Room3', 'Home1')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home1 Room1 Curtain1', 'Home1 Room1'),
	('Home1 Room1 Curtain2', 'Home1 Room1'),
	('Home1 Room1 Curtain3', 'Home1 Room1'),
	('Home1 Room2 Curtain1', 'Home1 Room2'),
	('Home1 Room2 Curtain2', 'Home1 Room2'),
	('Home1 Room2 Curtain3', 'Home1 Room2'),
	('Home1 Room3 Curtain1', 'Home1 Room3'),
	('Home1 Room3 Curtain2', 'Home1 Room3'),
	('Home1 Room3 Curtain3', 'Home1 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home1'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home1'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home1')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";

INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home1')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


-- ————————————————————————————————————— HOME HAS EVENT, INSERT HOME @ NEW TIME ————————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home2');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home2 Room1', 'Home2'),
	('Home2 Room2', 'Home2'),
	('Home2 Room3', 'Home2')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home2 Room1 Curtain1', 'Home2 Room1'),
	('Home2 Room1 Curtain2', 'Home2 Room1'),
	('Home2 Room1 Curtain3', 'Home2 Room1'),
	('Home2 Room2 Curtain1', 'Home2 Room2'),
	('Home2 Room2 Curtain2', 'Home2 Room2'),
	('Home2 Room2 Curtain3', 'Home2 Room2'),
	('Home2 Room3 Curtain1', 'Home2 Room3'),
	('Home2 Room3 Curtain2', 'Home2 Room3'),
	('Home2 Room3 Curtain3', 'Home2 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home2'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home2'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home2')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 04:00:00', 'Home2')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


-- ———————————————————————————————————— HOME HAS EVENT, INSERT ROOM AT SAME TIME ———————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home3');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home3 Room1', 'Home3'),
	('Home3 Room2', 'Home3'),
	('Home3 Room3', 'Home3')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home3 Room1 Curtain1', 'Home3 Room1'),
	('Home3 Room1 Curtain2', 'Home3 Room1'),
	('Home3 Room1 Curtain3', 'Home3 Room1'),
	('Home3 Room2 Curtain1', 'Home3 Room2'),
	('Home3 Room2 Curtain2', 'Home3 Room2'),
	('Home3 Room2 Curtain3', 'Home3 Room2'),
	('Home3 Room3 Curtain1', 'Home3 Room3'),
	('Home3 Room3 Curtain2', 'Home3 Room3'),
	('Home3 Room3 Curtain3', 'Home3 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home3'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home3'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home3')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "RoomsEvents" ("Rooms.id", "percentage", "time")
SELECT "Rooms"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home3 Room1')
) AS "T"("time", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


-- ———————————————————————————————————— HOME HAS EVENT,  INSERT ROOM AT NEW TIME ———————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home4');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home4 Room1', 'Home4'),
	('Home4 Room2', 'Home4'),
	('Home4 Room3', 'Home4')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home4 Room1 Curtain1', 'Home4 Room1'),
	('Home4 Room1 Curtain2', 'Home4 Room1'),
	('Home4 Room1 Curtain3', 'Home4 Room1'),
	('Home4 Room2 Curtain1', 'Home4 Room2'),
	('Home4 Room2 Curtain2', 'Home4 Room2'),
	('Home4 Room2 Curtain3', 'Home4 Room2'),
	('Home4 Room3 Curtain1', 'Home4 Room3'),
	('Home4 Room3 Curtain2', 'Home4 Room3'),
	('Home4 Room3 Curtain3', 'Home4 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home4'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home4'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home4')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "RoomsEvents" ("Rooms.id", "percentage", "time")
SELECT "Rooms"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 04:00:00', 'Home4 Room1')
) AS "T"("time", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


-- —————————————————————————————————— HOME HAS EVENT,  INSERT CURTAIN AT SAME TIME —————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home5');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home5 Room1', 'Home5'),
	('Home5 Room2', 'Home5'),
	('Home5 Room3', 'Home5')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home5 Room1 Curtain1', 'Home5 Room1'),
	('Home5 Room1 Curtain2', 'Home5 Room1'),
	('Home5 Room1 Curtain3', 'Home5 Room1'),
	('Home5 Room2 Curtain1', 'Home5 Room2'),
	('Home5 Room2 Curtain2', 'Home5 Room2'),
	('Home5 Room2 Curtain3', 'Home5 Room2'),
	('Home5 Room3 Curtain1', 'Home5 Room3'),
	('Home5 Room3 Curtain2', 'Home5 Room3'),
	('Home5 Room3 Curtain3', 'Home5 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home5'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home5'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home5')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "CurtainsEvents" ("Curtains.id", "percentage", "time")
SELECT "Curtains"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home5 Room1 Curtain1')
) AS "T"("time", "Curtains.name")
JOIN "Curtains" ON "T"."Curtains.name" = "Curtains"."name";


-- ——————————————————————————————————— HOME HAS EVENT, INSERT CURTAIN AT NEW TIME ——————————————————————————————————— --

INSERT INTO "Homes" ("name") VALUES
('Home6');

INSERT INTO "Rooms" ("name", "Homes.id")
SELECT "T"."name", "Homes"."id"
FROM
(
	VALUES
	('Home6 Room1', 'Home6'),
	('Home6 Room2', 'Home6'),
	('Home6 Room3', 'Home6')
) AS "T"("name", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "Curtains" ("name", "Rooms.id")
SELECT "T"."name", "Rooms"."id"
FROM
(
	VALUES
	('Home6 Room1 Curtain1', 'Home6 Room1'),
	('Home6 Room1 Curtain2', 'Home6 Room1'),
	('Home6 Room1 Curtain3', 'Home6 Room1'),
	('Home6 Room2 Curtain1', 'Home6 Room2'),
	('Home6 Room2 Curtain2', 'Home6 Room2'),
	('Home6 Room2 Curtain3', 'Home6 Room2'),
	('Home6 Room3 Curtain1', 'Home6 Room3'),
	('Home6 Room3 Curtain2', 'Home6 Room3'),
	('Home6 Room3 Curtain3', 'Home6 Room3')
) AS "T"("name", "Rooms.name")
JOIN "Rooms" ON "T"."Rooms.name" = "Rooms"."name";


INSERT INTO "HomesEvents" ("Homes.id", "percentage", "time")
SELECT "Homes"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 01:00:00', 'Home6'),
	(TIMESTAMP '2021-01-1 02:00:00', 'Home6'),
	(TIMESTAMP '2021-01-1 03:00:00', 'Home6')
) AS "T"("time", "Homes.name")
JOIN "Homes" ON "T"."Homes.name" = "Homes"."name";


INSERT INTO "CurtainsEvents" ("Curtains.id", "percentage", "time")
SELECT "Curtains"."id", 0, "T"."time"
FROM
(
	VALUES
	(TIMESTAMP '2021-01-1 04:00:00', 'Home6 Room1 Curtain1')
) AS "T"("time", "Curtains.name")
JOIN "Curtains" ON "T"."Curtains.name" = "Curtains"."name";


-- ———————————————————————————————————— ROOM HAS EVENT, INSERT HOME AT SAME TIME ———————————————————————————————————— --
-- ————————————————————————————————————— ROOM HAS EVENT,INSERT HOME AT NEW TIME ————————————————————————————————————— --
-- ———————————————————————————————————— ROOM HAS EVENT, INSERT ROOM AT SAME TIME ———————————————————————————————————— --
-- ————————————————————————————————————— ROOM HAS EVENT,INSERT ROOM AT NEW TIME ————————————————————————————————————— --
-- —————————————————————————————————— ROOM HAS EVENT,  INSERT CURTAIN AT SAME TIME —————————————————————————————————— --
-- ——————————————————————————————————— ROOM HAS EVENT, INSERT CURTAIN AT NEW TIME ——————————————————————————————————— --
-- —————————————————————————————————— CURTAIN HAS EVENT,  INSERT HOME AT SAME TIME —————————————————————————————————— --
-- ——————————————————————————————————— CURTAIN HAS EVENT, INSERT HOME AT NEW TIME ——————————————————————————————————— --
-- —————————————————————————————————— CURTAIN HAS EVENT,  INSERT ROOM AT SAME TIME —————————————————————————————————— --
-- ——————————————————————————————————— CURTAIN HAS EVENT, INSERT ROOM AT NEW TIME ——————————————————————————————————— --
-- ————————————————————————————————— CURTAIN HAS EVENT, INSERT CURTAIN AT SAME TIME ————————————————————————————————— --
-- —————————————————————————————————— CURTAIN HAS EVENT,INSERT CURTAIN AT NEW TIME —————————————————————————————————— --