
-- 	Created by: MPZinke
-- 	on 2020.12.19
--
-- 	DESCRIPTION: Main DB script for creating Curtain DB.
-- 	BUGS:
-- 	FUTURE:


SET client_min_messages TO WARNING;


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


CREATE UNIQUE INDEX ON "Homes"(REGEXP_REPLACE("name", '[^_\-a-zA-Z0-9]', ''))
  WHERE "is_deleted" = FALSE;


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
	UPDATE "HomesEvents" SET "is_deleted" = TRUE WHERE "Homes.id" = NEW."id";
	-- UPDATE "HomesOptions" SET "is_deleted" = TRUE WHERE "Homes.id" = NEW."id";
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
	UPDATE "RoomsEvents" SET "is_deleted" = TRUE WHERE "Rooms.id" = NEW."id";
	-- UPDATE "RoomsOptions" SET "is_deleted" = TRUE WHERE "Rooms.id" = NEW."id";
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


DROP FUNCTION IF EXISTS update_Curtains_deletion() CASCADE;
CREATE FUNCTION update_Curtains_deletion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "CurtainsEvents" SET "is_deleted" = TRUE WHERE "Curtains.id" = NEW."id";
	-- UPDATE "CurtainsOptions" SET "is_deleted" = TRUE WHERE "Curtains.id" = NEW."id";
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

DROP TABLE IF EXISTS "HomesEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "HomesEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


DROP TABLE IF EXISTS "RoomsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "RoomsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


DROP TABLE IF EXISTS "CurtainsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ———————————————————————————————————————————— EVENTS::INSERT INTEGRITY ———————————————————————————————————————————— --

-- ———— HomesEvents ———— --
DROP FUNCTION IF EXISTS insert_HomesEvent() CASCADE;
CREATE FUNCTION insert_HomesEvent() RETURNS TRIGGER AS $$
DECLARE
	"ExistingHomesEvent" INT = NULL;
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- If any RoomsEvents exist and are not deleted and have the home ID, mark as deleted
	UPDATE "RoomsEvents"
	SET "is_deleted" = TRUE
	WHERE "Rooms.id" IN
	(
		SELECT "Rooms"."id"
		FROM "Rooms"
		WHERE "Rooms"."Homes.id" = NEW."Homes.id"
	)
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "RoomsEvents"."is_deleted" = FALSE;

	-- If any CurtainsEvents exist and are not deleted and have the home ID, mark as deleted
	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "Curtains.id" IN
	(
		SELECT "Curtains"."id"
		FROM "Curtains"
		JOIN "Rooms" ON "Curtains"."Rooms.id" = "Rooms"."id"
		WHERE "Rooms"."Homes.id" = NEW."Homes.id"
	)
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "CurtainsEvents"."is_deleted" = FALSE;

	-- If HomesEvents exists for this time and is not deleted, return said event
	SELECT "id" INTO "ExistingHomesEvent"
	FROM "HomesEvents"
	WHERE "HomesEvents"."Homes.id" = NEW."Homes.id"
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "HomesEvents"."is_deleted" = FALSE;
	IF "ExistingHomesEvent" IS NOT NULL
	THEN
		-- FROM: https://stackoverflow.com/a/62655349
		PERFORM setval('"HomesEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "HomesEvents"));
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertHomesEventTrigger" ON "HomesEvents";
CREATE TRIGGER "InsertHomesEventTrigger"
  BEFORE INSERT ON "HomesEvents"
  FOR EACH ROW EXECUTE PROCEDURE insert_HomesEvent();


-- ———— RoomsEvents ———— --
DROP FUNCTION IF EXISTS insert_RoomsEvent() CASCADE;
CREATE FUNCTION insert_RoomsEvent() RETURNS TRIGGER AS $$
DECLARE
	"ExistingRoomsEvent" INT = NULL;
	"ExistingEventsCount" INT;
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- If any CurtainsEvents exist and are not deleted and have the home ID, mark as deleted
	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "Curtains.id" IN
	(
		SELECT "id"
		FROM "Curtains"
		WHERE "Rooms.id" = NEW."Rooms.id"
	)
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "CurtainsEvents"."is_deleted" = FALSE;

	-- If HomesEvents exists for this time and have the Rooms HomeID and is not deleted, raise Exception
	SELECT COUNT(*) INTO "ExistingEventsCount"
	FROM "HomesEvents"
	JOIN "Rooms" ON "HomesEvents"."Homes.id" = "Rooms"."Homes.id"
	WHERE "Rooms"."id" = NEW."Rooms.id"
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "HomesEvents"."is_deleted" = FALSE;
	IF "ExistingEventsCount" > 0
	THEN
		PERFORM setval('"RoomsEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "RoomsEvents"));
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	-- If RoomsEvents exists for this time and is not deleted, return OLD RoomsEvent ID
	SELECT * INTO "ExistingRoomsEvent"
	FROM "RoomsEvents"
	WHERE "RoomsEvents"."Rooms.id" = NEW."Rooms.id"
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "is_deleted" = FALSE;
	IF "ExistingRoomsEvent" IS NOT NULL
	THEN
		PERFORM setval('"RoomsEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "RoomsEvents"));
		RAISE 'A Room Event already exists for %', NEW."time";
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertRoomsEventTrigger" ON "RoomsEvents";
CREATE TRIGGER "InsertRoomsEventTrigger"
  BEFORE INSERT ON "RoomsEvents"
  FOR EACH ROW EXECUTE PROCEDURE insert_RoomsEvent();


-- ———— CurtainsEvents ———— --
DROP FUNCTION IF EXISTS insert_CurtainsEvent() CASCADE;
CREATE FUNCTION insert_CurtainsEvent() RETURNS TRIGGER AS $$
DECLARE
	"ExistingCurtainsEvent" RECORD = NULL;
	"ExistingEventsCount" INT;
BEGIN
	IF NEW."time" IS NULL
	THEN
		NEW."time" = CURRENT_TIMESTAMP;
	END IF;

	-- If HomesEvents exists for this time and have the Rooms HomeID and is not deleted, raise Exception
	SELECT COUNT(*) INTO "ExistingEventsCount"
	FROM "HomesEvents"
	WHERE "Homes.id" =
	(
		SELECT "Homes.id"
		FROM "Rooms"
		WHERE "id" =
		(
			SELECT "Rooms.id"
			FROM "Curtains"
			WHERE "id" = NEW."Curtains.id"
		)
	)
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "HomesEvents"."is_deleted" = FALSE;
	IF "ExistingEventsCount" > 0
	THEN
		PERFORM setval('"CurtainsEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "CurtainsEvents"));
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	-- If RoomsEvents exists for this time and have the Rooms HomeID and is not deleted, raise Exception
	SELECT COUNT(*) INTO "ExistingEventsCount"
	FROM "RoomsEvents"
	WHERE "Rooms.id" =
	(
		SELECT "Rooms.id"
		FROM "Curtains"
		WHERE "id" = NEW."Curtains.id"
	)
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "RoomsEvents"."is_deleted" = FALSE;
	IF "ExistingEventsCount" > 0
	THEN
		PERFORM setval('"CurtainsEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "CurtainsEvents"));
		RAISE 'A Room Event already exists for %', NEW."time";
	END IF;

	-- If CurtainsEvents exists for this time and is not deleted, return OLD CurtainsEvent ID
	SELECT * INTO "ExistingCurtainsEvent"
	FROM "CurtainsEvents"
	WHERE "CurtainsEvents"."id" = NEW."Curtains.id"
	  AND "time" < NEW."time" + INTERVAL '5 SECONDS'
	  AND NEW."time" - INTERVAL '5 SECONDS' < "time"
	  AND "is_deleted" = FALSE;
	IF "ExistingCurtainsEvent"."id" IS NOT NULL
	THEN
		PERFORM setval('"CurtainsEvents_id_seq"'::TEXT, (SELECT MAX("id") FROM "CurtainsEvents"));
		RAISE 'A Curtain Event already exists for %', NEW."time";
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "InsertCurtainsEventTrigger" ON "CurtainsEvents";
CREATE TRIGGER "InsertCurtainsEventTrigger"
  BEFORE INSERT ON "CurtainsEvents"
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
