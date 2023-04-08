
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




-- DROP TRIGGER IF EXISTS "DeleteOldCurtainEvents" ON "CurtainsEvents";
-- CREATE TRIGGER "DeleteOldCurtainEvents"
--   BEFORE SELECT ON "CurtainsEvents"
--   FOR EACH ROW
--   EXECUTE PROCEDURE update_old_CurtainsEvents();


-- ————————————————————————————————————————————————————— EVENTS ————————————————————————————————————————————————————— --
-- —————————————————————————————————————————————————————————————————————————————————————————————————————————————————— --

DROP TABLE IF EXISTS "HomesEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "HomesEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Homes.id" INT NOT NULL,
	FOREIGN KEY ("Homes.id") REFERENCES "Homes"("id"),
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	EXCLUDE USING GIST
	(
		"Homes.id" WITH =, 
		TSRANGE("time" - INTERVAL '5 SECONDS', "time" + INTERVAL '5 SECONDS') WITH &&
	)
	WHERE ("is_deleted" = FALSE)
);


DROP TABLE IF EXISTS "RoomsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "RoomsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Rooms.id" INT NOT NULL,
	FOREIGN KEY ("Rooms.id") REFERENCES "Rooms"("id"),
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	EXCLUDE USING GIST
	(
		"Rooms.id" WITH =, 
		TSRANGE("time" - INTERVAL '5 SECONDS', "time" + INTERVAL '5 SECONDS') WITH &&
	)
	WHERE ("is_deleted" = FALSE)
);


DROP TABLE IF EXISTS "CurtainsEvents" CASCADE;
CREATE TABLE IF NOT EXISTS "CurtainsEvents"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Curtains.id" INT NOT NULL,
	FOREIGN KEY ("Curtains.id") REFERENCES "Curtains"("id"),
	"Options.id" INT DEFAULT NULL,
	FOREIGN KEY ("Options.id") REFERENCES "Options"("id"),
	"is_activated" BOOLEAN NOT NULL DEFAULT FALSE,
	"is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,
	"percentage" INT NOT NULL,
	CHECK("percentage" >= 0),
	"time" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	EXCLUDE USING GIST
	(
		"Curtains.id" WITH =, 
		TSRANGE("time" - INTERVAL '5 SECONDS', "time" + INTERVAL '5 SECONDS') WITH &&
	)
	WHERE ("is_deleted" = FALSE)
);


CREATE UNIQUE INDEX ON "CurtainsEvents"("Curtains.id", "time")
  WHERE "is_deleted" = FALSE;


-- ———————————————————————————————————————————— EVENTS::INSERT INTEGRITY ———————————————————————————————————————————— --

DROP FUNCTION IF EXISTS update_for_HomesEvents_insertion() CASCADE;
CREATE FUNCTION update_for_HomesEvents_insertion() RETURNS TRIGGER AS $$
BEGIN
	UPDATE "RoomsEvents"
	SET "is_deleted" = TRUE
	WHERE "id" IN
	(
		SELECT "RoomsEvents"."id"
		FROM "RoomsEvents"
		JOIN "Rooms" ON "RoomsEvents"."Rooms.id" = "Rooms"."id"
		WHERE "Rooms"."Homes.id" = NEW."Homes.id"
		  AND "RoomsEvents"."is_deleted" = FALSE
		  AND NEW."time" < "RoomsEvents"."time" + INTERVAL '5 SECONDS'
		  AND "RoomsEvents"."time" - INTERVAL '5 SECONDS' < NEW."time"
	);

	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "id" IN
	(
		SELECT "CurtainsEvents"."id"
		FROM "CurtainsEvents"
		JOIN "Curtains" ON "CurtainsEvents"."Curtains.id" = "Curtains"."id"
		JOIN "Rooms" ON "Curtains"."Rooms.id" = "Rooms"."id"
		WHERE "Rooms"."Homes.id" = NEW."Homes.id"
		  AND "CurtainsEvents"."is_deleted" = FALSE
		  AND NEW."time" < "CurtainsEvents"."time" + INTERVAL '5 SECONDS'
		  AND "CurtainsEvents"."time" - INTERVAL '5 SECONDS' < NEW."time"
	);
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "UpdateForHomesEventsInsertionTrigger" ON "HomesEvents";
CREATE TRIGGER "UpdateForHomesEventsInsertionTrigger"
  BEFORE INSERT ON "HomesEvents"
  FOR EACH ROW
  EXECUTE PROCEDURE update_for_HomesEvents_insertion();


DROP FUNCTION IF EXISTS update_for_RoomsEvents_insertion() CASCADE;
CREATE FUNCTION update_for_RoomsEvents_insertion() RETURNS TRIGGER AS $$
DECLARE
	"HomesEvents_Count" INT;
BEGIN
	-- Check if any Home Events already exist
	SELECT COUNT("HomesEvents"."id") INTO "HomesEvents_Count"
	FROM "HomesEvents"
	JOIN "Homes" ON "HomesEvents"."Homes.id" = "Homes"."id"
	JOIN "Rooms" ON "Homes"."id" = "Rooms"."Homes.id"
	WHERE "Rooms"."id" = NEW."Rooms.id"
	  AND "HomesEvents"."is_deleted" = FALSE
	  AND NEW."time" < "HomesEvents"."time" + INTERVAL '5 SECONDS'
	  AND "HomesEvents"."time" - INTERVAL '5 SECONDS' < NEW."time";
	IF "HomesEvents_Count" > 0
	THEN
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	UPDATE "CurtainsEvents"
	SET "is_deleted" = TRUE
	WHERE "id" IN
	(
		SELECT "CurtainsEvents"."id"
		FROM "CurtainsEvents"
		JOIN "Curtains" ON "CurtainsEvents"."Curtains.id" = "Curtains"."id"
		WHERE "Curtains"."Rooms.id" = NEW."Rooms.id"
		  AND "CurtainsEvents"."is_deleted" = FALSE
		  AND NEW."time" < "CurtainsEvents"."time" + INTERVAL '5 SECONDS'
		  AND "CurtainsEvents"."time" - INTERVAL '5 SECONDS' < NEW."time"
	);

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "UpdateForRoomsEventsInsertionTrigger" ON "RoomsEvents";
CREATE TRIGGER "UpdateForRoomsEventsInsertionTrigger"
  BEFORE INSERT ON "RoomsEvents"
  FOR EACH ROW
  EXECUTE PROCEDURE update_for_RoomsEvents_insertion();


DROP FUNCTION IF EXISTS update_for_CurtainsEvents_insertion() CASCADE;
CREATE FUNCTION update_for_CurtainsEvents_insertion() RETURNS TRIGGER AS $$
DECLARE
	"HomesEvents_Count" INT;
	"RoomsEvents_Count" INT;
BEGIN
	-- Check if any Home Events already exist
	SELECT COUNT("HomesEvents"."id") INTO "HomesEvents_Count"
	FROM "HomesEvents"
	JOIN "Homes" ON "HomesEvents"."Homes.id" = "Homes"."id"
	JOIN "Rooms" ON "Homes"."id" = "Rooms"."Homes.id"
	JOIN "Curtains" ON "Rooms"."id" = "Curtains"."Rooms.id"
	WHERE "Curtains"."id" = NEW."Curtains.id"
	  AND "HomesEvents"."is_deleted" = FALSE
	  AND NEW."time" < "HomesEvents"."time" + INTERVAL '5 SECONDS'
	  AND "HomesEvents"."time" - INTERVAL '5 SECONDS' < NEW."time";
	IF "HomesEvents_Count" > 0
	THEN
		RAISE 'A Home Event already exists for %', NEW."time";
	END IF;

	-- Check if any Room Events already exist
	SELECT COUNT("RoomsEvents"."id") INTO "RoomsEvents_Count"
	FROM "RoomsEvents"
	JOIN "Rooms" ON "RoomsEvents"."Rooms.id" = "Rooms"."id"
	JOIN "Curtains" ON "Rooms"."id" = "Curtains"."Rooms.id"
	WHERE "Curtains"."id" = NEW."Curtains.id"
	  AND "RoomsEvents"."is_deleted" = FALSE
	  AND NEW."time" < "RoomsEvents"."time" + INTERVAL '5 SECONDS'
	  AND "RoomsEvents"."time" - INTERVAL '5 SECONDS' < NEW."time";
	IF "RoomsEvents_Count" > 0
	THEN
		RAISE 'A Room Event already exists for %', NEW."time";
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;


DROP TRIGGER IF EXISTS "UpdateForCurtainsEventsInsertionTrigger" ON "CurtainsEvents";
CREATE TRIGGER "UpdateForCurtainsEventsInsertionTrigger"
  BEFORE INSERT ON "CurtainsEvents"
  FOR EACH ROW
  EXECUTE PROCEDURE update_for_CurtainsEvents_insertion();


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
