
-- 	Created by: MPZinke
-- 	on 2020.12.19
--
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


CREATE EXTENSION btree_gist;



-- ————————————————————————————————————————————————————— AREAS  ————————————————————————————————————————————————————— --
-- —————————————————————————————————————————————————————————————————————————————————————————————————————————————————— --

DROP TABLE IF EXISTS "Homes" CASCADE;
CREATE TABLE IF NOT EXISTS "Homes"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL
);


CREATE UNIQUE INDEX ON "Homes"("name")
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "Rooms" CASCADE;
CREATE TABLE IF NOT EXISTS "Rooms"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id")
);


CREATE UNIQUE INDEX ON "Rooms"("Homes.id", REGEXP_REPLACE("name", '[^_\-a-zA-Z0-9]', ''))
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "Curtains" CASCADE;
CREATE TABLE IF NOT EXISTS "Curtains"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"buffer_time" INT NOT NULL DEFAULT 0,  -- seconds
	"direction" BOOLEAN DEFAULT NULL,  -- NULL if curtain should use hardcoded values otherwise valued
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"length" INT DEFAULT NULL,  -- NULL if curtain should use hardcoded values otherwise valued
	CHECK("length" > 0 OR "length" IS NULL),
	"name" VARCHAR(32) NOT NULL,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id")
);


CREATE UNIQUE INDEX ON "Curtains"("Rooms.id", REGEXP_REPLACE("name", '[^_\-a-zA-Z0-9]', ''))
  WHERE "is_deleted" = FALSE;


DROP FUNCTION IF EXISTS update_old_CurtainsEvents() CASCADE;
CREATE FUNCTION update_old_CurtainsEvents() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "CurtainsEvents" SET "is_deleted" = TRUE WHERE "time" < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- ———————————————————————————————————————————— AREAS::DELETE  INTEGRITY ———————————————————————————————————————————— --

DROP FUNCTION IF EXISTS update_Homes_deletion() CASCADE;
CREATE FUNCTION update_Homes_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "Rooms" SET "is_deleted" = TRUE WHERE "Homes.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteHomesTrigger" ON "Homes";
CREATE TRIGGER "DeleteHomesTrigger"
  AFTER UPDATE ON "Homes"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Homes_deletion();


DROP FUNCTION IF EXISTS update_Rooms_deletion() CASCADE;
CREATE FUNCTION update_Rooms_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "Curtains" SET "is_deleted" = TRUE WHERE "Rooms.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteRoomsTrigger" ON "Rooms";
CREATE TRIGGER "DeleteRoomsTrigger"
  AFTER UPDATE ON "Rooms"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Rooms_deletion();


-- ———————————————————————————————————————————————————— OPTIONS  ———————————————————————————————————————————————————— --
-- —————————————————————————————————————————————————————————————————————————————————————————————————————————————————— --

DROP TABLE IF EXISTS "Options" CASCADE;
CREATE TABLE IF NOT EXISTS "Options"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"description" VARCHAR(256) NOT NULL DEFAULT '',
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"name" VARCHAR(32) NOT NULL UNIQUE
);


DROP TABLE IF EXISTS "HomesOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "HomesOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Homes.id", "Options.id")
);


DROP TABLE IF EXISTS "RoomsOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "RoomsOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Rooms.id", "Options.id")
);


DROP TABLE IF EXISTS "CurtainsOptions" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsOptions"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT NOT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"data" JSON DEFAULT NULL,
	"is_on" BOOLEAN NOT NULL,
	"notes" VARCHAR(256) NOT NULL DEFAULT '',
	UNIQUE ("Curtains.id", "Options.id")
);


-- ——————————————————————————————————————————— OPTIONS::DELETE INTEGRITY  ——————————————————————————————————————————— --



-- ————————————————————————————————————————————————————— EVENTS ————————————————————————————————————————————————————— --
-- —————————————————————————————————————————————————————————————————————————————————————————————————————————————————— --


DROP TABLE IF EXISTS "Events" CASCADE;
CREATE TABLE IF NOT EXISTS "Events"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE("Options.id", "percentage", "time")
);


DROP TABLE IF EXISTS "HomesEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "HomesEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id"),
	"Events.id" INT NOT NULL,
	FOREIGN KEY ("Events.id") REFERENCES "Events"("id"),
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE UNIQUE INDEX ON "HomesEvents"("Homes.id", "Events.id")
  WHERE "is_deleted" = FALSE;


DROP TABLE IF EXISTS "RoomsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "RoomsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id"),
	"Events.id" INT NOT NULL,
	FOREIGN KEY ("Events.id") REFERENCES "Events"("id"),
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE
);


DROP TABLE IF EXISTS "CurtainsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Events.id" INT NOT NULL,
	FOREIGN KEY ("Events.id") REFERENCES "Events"("id"),
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE
);



-- ———————————————————————————————————————————— EVENTS::INSERT INTEGRITY ———————————————————————————————————————————— --

-- ———— HomesEvents ———— --

DROP VIEW IF EXISTS "HomesEventsView";
CREATE VIEW "HomesEventsView" AS
SELECT "HomesEvents".*, "Events"."is_activated", "Events"."Options.id", "Events"."percentage", "Events"."time"
FROM "HomesEvents"
JOIN "Events" ON "HomesEvents"."Events.id" = "Events"."id"
WHERE "HomesEvents"."is_deleted" = FALSE;


DROP FUNCTION IF EXISTS insert_HomesEvent() CASCADE;
CREATE FUNCTION insert_HomesEvent() RETURNS TRIGGER AS $$
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- Determine if an event exists
	SELECT "id" INTO NEW."Events.id"
	FROM "Events"
	WHERE "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time";

	-- If event does not exist, create it
	IF NEW."Events.id" IS NULL
	THEN
		INSERT INTO "Events" ("Options.id", "percentage", "time") VALUES
		(NEW."Options.id", NEW."percentage", NEW."time")
		RETURNING "id" INTO NEW."Events.id";
	END IF;

	UPDATE "HomesEvents"
	SET "is_deleted" = TRUE
	WHERE "HomesEvents"."Events.id" = NEW."Events.id";

	UPDATE "RoomsEvents"
	SET "is_deleted" = TRUE
	WHERE "RoomsEvents"."Events.id" = NEW."Events.id";

	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "CurtainsEvents"."Events.id" = NEW."Events.id";

	INSERT INTO "HomesEvents"("Homes.id", "Events.id") VALUES
	(NEW."Homes.id", NEW."Events.id") RETURNING "id" INTO NEW."id";

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertHomesEventTrigger" ON "HomesEvents";
CREATE TRIGGER "InsertHomesEventTrigger"
  INSTEAD OF INSERT ON "HomesEventsView"
  FOR EACH ROW EXECUTE PROCEDURE insert_HomesEvent();


-- ———— RoomsEvents ———— --

DROP VIEW IF EXISTS "RoomsEventsView";
CREATE VIEW "RoomsEventsView" AS
SELECT "RoomsEvents".*, "Events"."is_activated", "Events"."Options.id", "Events"."percentage", "Events"."time"
FROM "RoomsEvents"
JOIN "Events" ON "RoomsEvents"."Events.id" = "Events"."id"
WHERE "RoomsEvents"."is_deleted" = FALSE;


DROP FUNCTION IF EXISTS insert_RoomsEvent() CASCADE;
CREATE FUNCTION insert_RoomsEvent() RETURNS TRIGGER AS $$
DECLARE
	"HomesEventsCount" INT;
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- Determine if an event exists
	SELECT "id" INTO NEW."Events.id"
	FROM "Events"
	WHERE "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time";

	-- If event does not exist, create it
	IF NEW."Events.id" IS NULL
	THEN
		INSERT INTO "Events" ("Options.id", "percentage", "time") VALUES
		(NEW."Options.id", NEW."percentage", NEW."time")
		RETURNING "id" INTO NEW."Events.id";
	END IF;

	SELECT COUNT("HomesEvents"."id") INTO "HomesEventsCount"
	FROM "HomesEvents"
	WHERE "Homes.id" = (SELECT "Homes.id" FROM "Rooms" WHERE "id" = NEW."Rooms.id")
	  AND "Events.id" = NEW."Events.id";
	IF "HomesEventsCount" > 0
	THEN
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	UPDATE "RoomsEvents"
	SET "is_deleted" = TRUE
	WHERE "RoomsEvents"."Events.id" = NEW."Events.id";

	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "CurtainsEvents"."Events.id" = NEW."Events.id";

	INSERT INTO "RoomsEvents"("Rooms.id", "Events.id") VALUES
	(NEW."Rooms.id", NEW."Events.id") RETURNING "id" INTO NEW."id";

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertRoomsEventTrigger" ON "RoomsEvents";
CREATE TRIGGER "InsertRoomsEventTrigger"
  INSTEAD OF INSERT ON "RoomsEventsView"
  FOR EACH ROW EXECUTE PROCEDURE insert_RoomsEvent();


-- ———— CurtainsEvents ———— --

DROP VIEW IF EXISTS "CurtainsEventsView";
CREATE VIEW "CurtainsEventsView" AS
SELECT "CurtainsEvents".*, "Events"."is_activated", "Events"."Options.id", "Events"."percentage", "Events"."time"
FROM "CurtainsEvents"
JOIN "Events" ON "CurtainsEvents"."Events.id" = "Events"."id"
WHERE "CurtainsEvents"."is_deleted" = FALSE;


DROP FUNCTION IF EXISTS insert_CurtainsEvent() CASCADE;
CREATE FUNCTION insert_CurtainsEvent() RETURNS TRIGGER AS $$
DECLARE
	"HomesEventsCount" INT;
	"RoomsEventsCount" INT;
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- Determine if an event exists
	SELECT "id" INTO NEW."Events.id"
	FROM "Events"
	WHERE "time" = NEW."time";

	-- If event does not exist, create it
	IF NEW."Events.id" IS NULL
	THEN
		INSERT INTO "Events" ("Options.id", "percentage", "time") VALUES
		(NEW."Options.id", NEW."percentage", NEW."time")
		RETURNING "id" INTO NEW."Events.id";
	END IF;

	SELECT COUNT("HomesEvents"."id") INTO "HomesEventsCount"
	FROM "HomesEvents"
	WHERE "Homes.id" = 
		(
			SELECT "Homes.id" FROM
			(
				SELECT "Rooms.id" FROM "Curtains" WHERE "id" = NEW."Curtains.id"
			) AS "HomeQuery"
			WHERE "HomeQuery"."id" = NEW."Rooms.id"
		)
	  AND "Events.id" = NEW."Events.id";
	IF "HomesEventsCount" > 0
	THEN
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	SELECT COUNT("RoomsEvents"."id") INTO "RoomsEventsCount"
	FROM "RoomsEvents"
	WHERE "Rooms.id" = (SELECT "Rooms.id" FROM "Curtains" WHERE "id" = NEW."Curtains.id")
	  AND "Events.id" = NEW."Events.id";
	IF "RoomsEventsCount" > 0
	THEN
		RAISE 'A Room Event already exists for %', NEW."time";
	END IF;

	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "CurtainsEvents"."Events.id" = NEW."Events.id";

	INSERT INTO "CurtainsEvents"("Curtains.id", "Events.id") VALUES
	(NEW."Curtains.id", NEW."Events.id") RETURNING "id" INTO NEW."id";

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertCurtainsEventTrigger" ON "CurtainsEvents";
CREATE TRIGGER "InsertCurtainsEventTrigger"
  INSTEAD OF INSERT ON "CurtainsEventsView"
  FOR EACH ROW EXECUTE PROCEDURE insert_CurtainsEvent();


-- ———————————————————————————————————————————— EVENTS::UPDATE INTEGRITY ———————————————————————————————————————————— --


-- ———————————————————————————————————————————— EVENTS::DELETE INTEGRITY ———————————————————————————————————————————— --

DROP FUNCTION IF EXISTS update_Homes_deletion() CASCADE;
CREATE FUNCTION update_Homes_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "HomesEvents" SET "is_deleted" = TRUE WHERE "Homes.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete HomesEvents & HomesOptions when Home is deleted.
DROP TRIGGER IF EXISTS "DeleteHomesTrigger" ON "Homes";
CREATE TRIGGER "DeleteHomesTrigger"
  AFTER UPDATE ON "Homes"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Homes_deletion();


DROP FUNCTION IF EXISTS update_Rooms_deletion() CASCADE;
CREATE FUNCTION update_Rooms_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "RoomsEvents" SET "is_deleted" = TRUE WHERE "Rooms.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete RoomsEvents & RoomsOptions when Room is deleted.
DROP TRIGGER IF EXISTS "DeleteRoomsTrigger" ON "Rooms";
CREATE TRIGGER "DeleteRoomsTrigger"
  AFTER UPDATE ON "Rooms"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Rooms_deletion();



DROP FUNCTION IF EXISTS update_Curtains_deletion() CASCADE;
CREATE FUNCTION update_Curtains_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "CurtainsEvents" SET "is_deleted" = TRUE WHERE "Curtains.id" = NEW."id";
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


-- Delete CurtainsEvents & CurtainsOptions when Curtain is deleted.
DROP TRIGGER IF EXISTS "DeleteCurtainsTrigger" ON "Curtains";
CREATE TRIGGER "DeleteCurtainsTrigger"
  AFTER UPDATE ON "Curtains"
  FOR EACH ROW
  WHEN (NEW."is_deleted" = TRUE)
  EXECUTE PROCEDURE update_Curtains_deletion();
